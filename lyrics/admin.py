from django.contrib import admin
from .models import Lyric, Comment
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Lyric)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('song_name', 'slug', 'status', 'created_on')
    search_fields = ['song_name','lyrics']
    list_filter = ('status','created_on',)
    prepopulated_fields = {'slug': ('song_name',)}
    summernote_fields = ('lyrics',)



# Register your models here.

admin.site.register(Comment)

