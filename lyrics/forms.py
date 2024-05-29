from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text',)

class LyricSearchForm(forms.Form):
    q = forms.CharField(label='Search for lyrics', max_length=100)