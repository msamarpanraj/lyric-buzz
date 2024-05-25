from . import views
from django.urls import path

urlpatterns = [
    path('', views.LyricList.as_view(), name='home'),
]