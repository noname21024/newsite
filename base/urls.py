from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name = 'home'),
    path('manga-list/', views.manga_list, name = 'manga-list'),
    
    path('login/', views.loginPage, name = 'login'),
    path('register/', views.registerPage, name= 'register'),
    path('logout/', views.logoutPage, name = 'logout'),

    # manga
    path('manga_room/<str:name>/', views.MangaRoom, name = 'manga-room' ),
    path('manga/<str:name>/chapter-<str:pk>/', views.Manga, name = 'manga'),
    path('upload_manga/', views.upload_manga, name = 'upload-manga'),
    path('add-chapter/<str:name>/', views.upload_chapter, name = 'add-chapter'),
    path('upload_images/<str:name>/chapter-<int:pk>/', views.upload_images, name ='upload-images'),
    path('delete_manga/<int:pk>/', views.delete_manga, name = 'delete-manga'),
    path('update_manga/<int:pk>/', views.update_manga, name = 'update-manga'),

    # userpage
    path('user_page/', views.user_page, name = 'user-page'),
    path('change_user_page/', views.change_user_page, name = 'change-user-page'),
    path('follow_manga/', views.follow_manga_userpage, name = 'follow-manga-userpage'),

    # htmx-patterns
    path('check_username/', views.check_username, name = 'check-username'),
    path('search-manga/', views.search_manga, name = 'search-manga'),
    path('follow-manga/<int:pk>/', views.follow_manga, name = 'follow-manga'),
]

# redirect
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
