from base.models import MangaUpload
from django.contrib.auth.models import User


def run():
    user = User.objects.first()
    manga = MangaUpload.objects.first()

    user.manga_follows.add(manga)
    print(user.manga_follows.all())