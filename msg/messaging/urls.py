
from django.contrib import admin
from django.urls import path
from . import views
from django.urls import include, path
from .views import fetch_user_list
from .views import protected_media
from django.conf import settings
from django.conf.urls.static import static
from .views import MessageView

urlpatterns = [
    path('', views.home),
    path("login/", views.user_login),
    path('register/',views.register),
    path('profile/', views.profile, name='profile'),
    path('messages/<str:username>/', MessageView, name='fetch_messages'),
    path('logout/',views.logout_view),
    path('chat/',views.chat),
path('messages_list/users',views.user_messages),
    path('users/', fetch_user_list, name='fetch_user_list'),
    path('media/<path:file_path>/', protected_media, name='protected_media'),
]
