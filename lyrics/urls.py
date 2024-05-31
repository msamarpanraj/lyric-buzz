from . import views
from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path("about/", include("about.urls"), name="about-urls"),
    path('', views.LyricList.as_view(), name='home'),
    path('search/', views.search_lyrics, name='search_lyrics'),
    path('lyrics/', views.AllLyricsList.as_view(), name='lyrics_list'),
    path('submit/', views.submit_lyric, name='submit_lyric'),
    path('profile/', views.profile, name='profile'),
    path('edit/<slug:slug>/', views.edit_lyric, name='edit_lyric'),
    path('delete/<slug:slug>/', views.delete_lyric, name='delete_lyric'),
    path('<slug:slug>/', views.lyric_detail, name='lyric_detail'),
    path('like/<slug:slug>/', views.like_lyric, name='like_lyric'),
    path('<slug:slug>/edit_comment/<int:comment_id>', views.comment_edit, name='comment_edit'),
    path('<slug:slug>/delete_comment/<int:comment_id>', views.comment_delete, name='comment_delete'),
]



