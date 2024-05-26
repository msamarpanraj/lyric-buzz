from . import views
from django.urls import path

urlpatterns = [
    path('', views.LyricList.as_view(), name='home'),
    path('<slug:slug>/', views.lyric_detail, name='lyric_detail'),

]