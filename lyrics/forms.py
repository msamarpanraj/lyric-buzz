from .models import Comment, Lyric
from django import forms
from django_summernote.widgets import SummernoteWidget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text',)

class LyricSearchForm(forms.Form):
    q = forms.CharField(label='Search for lyrics', max_length=100)


class LyricSubmissionForm(forms.ModelForm):
    class Meta:
        model = Lyric
        fields = ['song_name', 'slug', 'lyric_writer', 'album', 'featured_image', 'lyrics']
        widgets = {
            'lyrics': SummernoteWidget(),
        }


