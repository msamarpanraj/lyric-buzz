from . import views
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("about/", include("about.urls"), name="about-urls"),
    path('', views.LyricList.as_view(), name='home'),
    path('search/', views.search_lyrics, name='search_lyrics'),
    path('lyrics/', views.AllLyricsList.as_view(), name='lyrics_list'),
    path('<slug:slug>/', views.lyric_detail, name='lyric_detail'),
    path('<slug:slug>/edit_comment/<int:comment_id>',
         views.comment_edit, name='comment_edit'),
    path('<slug:slug>/delete_comment/<int:comment_id>',
         views.comment_delete, name='comment_delete'),
]
