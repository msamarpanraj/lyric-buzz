from django.shortcuts import render
from django.views import generic
from .models import Lyric


# Create your views here.

class LyricList(generic.ListView):
     queryset = Lyric.objects.all()
     template_name = "lyric_list.html"