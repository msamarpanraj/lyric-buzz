from .models import Comment, Lyric, Profile
from django import forms
from django_summernote.widgets import SummernoteWidget
from django.contrib.auth.models import User



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

class ProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(label='Profile Image', required=False, widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ['profile_image', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'maxlength': '500'}),  # assuming you want a 500 character limit
        }
        