from django.contrib import admin
from .models import MangaUpload, Rating, Chapter, UploadMutipleImages, Profile, Message
# Register your models here.
admin.site.register(Profile)
admin.site.register(Message)

@admin.register(MangaUpload)
class MangaUploadAdmin(admin.ModelAdmin):
      list_display = ['title', 'get_tags']

      def get_tags(self, obj):
            return ", ".join( o for o in obj.tags.names())

admin.site.register(Rating)
@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
      list_display = ['manga', 'chapter']

admin.site.register(UploadMutipleImages)
      