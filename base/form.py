from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import MangaUpload, Chapter, UploadMutipleImages, Profile

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class MangaUploadForm(ModelForm):
    class Meta:
        model = MangaUpload
        fields = '__all__'

class ChapterForm(ModelForm):
    class Meta:
        model = Chapter
        fields = '__all__'

class UploadMutipleImagesForm(ModelForm):
    class Meta:
        model = UploadMutipleImages
        fields = '__all__'

class ChapterForm(ModelForm):
    class Meta:
        model = Chapter
        fields = '__all__'