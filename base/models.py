from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image

# manga
# user
# rating
# chapter

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(upload_to='profile_picture/', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 and img.width > 300:
            outputsize = (300, 300)
            img.thumbnail(outputsize)
            img.save(self.image.path)

class MangaUpload(models.Model):

    title = models.CharField(max_length= 200)
    description = models.TextField(max_length = 1000)
    image = models.ImageField(upload_to='manga_images/')
    secondary_name = models.CharField(max_length = 200)
    tags = TaggableManager()       
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    follower = models.ManyToManyField(User, related_name = 'manga_follows', blank = True, symmetrical=False)

    class Meta:
        ordering = ['-created', '-updated'] 

    def __str__(self):
        return self.title

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    manga = models.ForeignKey(MangaUpload, on_delete = models.CASCADE, related_name = 'ratings')
    rating = models.PositiveSmallIntegerField(validators = [MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f'Rating: {self.rating}'

class Chapter(models.Model):
    manga = models.ForeignKey(MangaUpload, on_delete = models.CASCADE, related_name = 'chapters')
    chapter = models.IntegerField()
    name = models.CharField(max_length = 200, blank = True, null = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.chapter}'

class UploadMutipleImages(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete = models.CASCADE, related_name = 'images')
    images = models.FileField(upload_to='manga-chapter-images/')
    manga = models.ForeignKey(MangaUpload, on_delete = models.CASCADE)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    manga = models.ForeignKey(MangaUpload, on_delete = models.CASCADE, related_name = 'messages')
    chapter = models.ForeignKey(Chapter, on_delete = models.CASCADE, null = True, blank = True, related_name = 'messages')
    body = models.TextField()
    update = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-created', '-update']

    def __str__(self):
        return f'message of {self.manga.title} in chapter {self.chapter}'
