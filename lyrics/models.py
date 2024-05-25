from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "Draft"), (1, "Published"))

# Create your models here.
class Lyric(models.Model):
    song_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    lyric_writer = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    lyrics = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_lyrics')
   
    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.song_name} | Posted by {self.user}"

class Comment(models.Model):
    lyric = models.ForeignKey(
        Lyric, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter")
    comment_text = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

