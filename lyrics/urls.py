from . import views
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("about/", include("about.urls"), name="about-urls"),
    path('', views.LyricList.as_view(), name='home'),
    path('<slug:slug>/', views.lyric_detail, name='lyric_detail'),

]
