from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .form import LoginForm, MangaUploadForm, ChapterForm, ProfileForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import MangaUpload, Chapter, UploadMutipleImages, Profile, Message
from taggit.models import Tag
from django.core.paginator import Paginator
from django.db.models import Max

# home page

def home(request):
    tags = Tag.objects.all()
    mangas = MangaUpload.objects.annotate(max_created = Max('chapters__created')).order_by('-max_created')
    page = Paginator(mangas, 12)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    context = {
        'tags': tags,
        'pages': page
    }

    return render(request, 'base/home.html', context)

def manga_list(request):
    q = request.GET.get('q')
    if q != None:
        tag = Tag.objects.get(name = q)
        mangas = MangaUpload.objects.filter(tags= tag).annotate(max_created = Max('chapters__created')).order_by('-max_created')
    else:
        mangas = MangaUpload.objects.all().annotate(max_created = Max('chapters__created')).order_by('-max_created')
    page = Paginator(mangas, 36)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    tags = Tag.objects.all()
    context = {
        'tags': tags,
        'pages': page
    }
    
    return render(request, 'base/home.html', context)

def search_manga(request):
    search_text = request.POST.get('search') if request.POST.get('search') != None else '' 
    results = MangaUpload.objects.filter(title__icontains = search_text)
    context = {'results': results}

    return render(request, 'base/manga-results.html', context)

# user page

def user_page(request):
    tags = Tag.objects.all()

    if request.method == 'POST':
        name = request.POST['name']
        manga = MangaUpload.objects.get(title = name)
        action = request.POST['follow']
        current_manga = request.user.manga_follows
        if action == 'unfollow':
            current_manga.remove(manga)

        return render(request, 'base/general-information.html', {'tags': tags})    

    return render(request, 'base/general-information.html', {'tags': tags})


def loginPage(request):
    form = LoginForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            pass

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')

    context = {'form': form, 'type': 'login'}
    return render(request, 'base/login_register.html', context)

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form.errors)
        if form.is_valid():
            user = form.save(commit = False)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('no bi loi')

    context = {'form': form}
    return render(request, 'base/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def check_username(request):
    username = request.POST.get('username')

    if get_user_model().objects.filter(username = username).exists():
        return HttpResponse('<div style = "color: lightgreen; padding:0 10px">no co ton tai</div>')
    else:
        return HttpResponse('<div style = "color: red; padding:0 10px">no dell ton tai</div>')

def change_user_page(request):
    if request.method == 'POST':
        u_form = UserForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        print(u_form.errors)
        print(p_form.errors)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save() 
            p_form.save()
            return redirect('change-user-page')
    else:
        u_form = UserForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)

    context = {'u_form':u_form, 'p_form':p_form}

    return render(request, 'base/Change-account-information.html', context)

def follow_manga_userpage(request):
    if request.method == 'POST':
        name = request.POST['name']
        manga = MangaUpload.objects.get(title = name)
        action = request.POST['follow']
        current_manga = request.user.manga_follows
        if action == 'unfollow':
            current_manga.remove(manga)
        
        return render(request, 'base/story-is-following.html')    

    return render(request, 'base/story-is-following.html')
    
# manga room
def MangaRoom(request, name):
    manga = MangaUpload.objects.get(title = name)
    tags = Tag.objects.all()
    chapters = manga.chapters.all()
    first_chapter = manga.chapters.last()
    end_chapter = manga.chapters.first()
    messages = manga.messages.all()
    count =  messages.count()

    if request.method == 'POST':
        value = request.POST['value']
        if value == 'message':
            Message.objects.create(
                user = request.user, 
                manga = manga, 
                body = request.POST.get('body')
            )
            return redirect('manga-room', name)
        else:
            current_manga = request.user.manga_follows
            action = request.POST['follow']
            if action == 'unfollow':
                current_manga.remove(manga)
            elif action == 'follow':
                current_manga.add(manga)
            

    context = {'manga': manga, 'tags': tags, 'chapters': chapters, 'first_chapter': first_chapter, 'end_chapter': end_chapter, 'messages': messages, 'count': count}

    return render(request, 'base/manga_room.html',context)

def Manga(request, name, pk):
    manga = MangaUpload.objects.get(title = name)
    chapter = manga.chapters.get(chapter = pk)
    images = chapter.images.all()
    messages = chapter.messages.all()
    count = messages.count()

    if request.method == 'POST':
        Message.objects.create(
            user = request.user,
            manga = manga,
            chapter = chapter,
            body = request.POST.get('body')
        )

        return redirect('manga', name, pk)

    context = {'images': images, 'manga': manga, 'chapter': chapter, 'messages': messages, 'count': count}

    return render(request, 'base/manga.html', context)

def upload_manga(request):
    form = MangaUploadForm()
    type = 'upload_manga'

    if request.method == 'POST':
        form = MangaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return HttpResponse('post ko hop le')
        
    context = {'form': form, type: type}

    return render(request, 'base/upload_manga.html', context)

def upload_chapter(request, name):
    type = 'chapter'

    manga = MangaUpload.objects.get(title = name)
    form = ChapterForm()
    
    if request.method == 'POST':
        name = request.POST.get('namechapter')
        chapter = request.POST.get('chapter')

        obj, bol = Chapter.objects.get_or_create(manga = manga, chapter = chapter, name = name)

        obj.save()

        return redirect('upload-images', manga.title, chapter)

    context = {'form': form, 'type': type, 'name' : manga.title}

    return render(request, 'base/upload_chapter.html', context)

def upload_images(request, name, pk):
    type = 'images'

    manga = MangaUpload.objects.get(title = name)
    chapter = manga.chapters.get(chapter = pk)

    if request.method == 'POST':
        files = request.FILES.getlist("uploadfiles")
        for f in files:
            obj= UploadMutipleImages(manga = manga, chapter = chapter, images = f).save()

        return redirect('manga-room', manga.title)

    context = {'type': type, 'name': name}
    return render(request, 'base/upload_chapter.html', context)

def delete_manga(request, pk):
    manga = MangaUpload.objects.get(id = pk)

    if request.method == 'POST':
        manga.delete()
        return redirect('home')

    return render(request, 'base/delete_manga.html', {'obj': manga})

def update_manga(request, pk):
    manga = MangaUpload.objects.get(id = pk)
    form = MangaUploadForm(instance=manga)

    if request.method == 'POST':
        form = MangaUploadForm(request.POST, request.FILES, instance=manga)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}

    return render(request, 'base/upload_manga.html', context)

def follow_manga(request, pk):
    user = request.user
    manga = MangaUpload.objects.get(id = pk)
    user.mangas.add(manga)

