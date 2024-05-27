from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from .models import Lyric
from .forms import CommentForm


# Create your views here.

class LyricList(generic.ListView):
     queryset = Lyric.objects.filter(status=1)
     template_name = "lyrics/index.html"
     paginate_by = 6


def lyric_detail(request, slug):
    """
    Display an individual :model:`lyrics.Lyric`.

    **Context**

    ``lyric``
        An instance of :model:`lyrics.Lyric`.

    **Template:**

    :template:`lyrics/lyric_detail.html`
    """

    queryset = Lyric.objects.filter(status=1)
    lyric = get_object_or_404(queryset, slug=slug)
    comments = lyric.comments.all().order_by("-created_on")
    comment_count = lyric.comments.filter(approved=True).count()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if  comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.lyric = lyric
            comment.save()
            messages.add_message(
        request, messages.SUCCESS,
        'Comment submitted and awaiting approval'
    )

    comment_form = CommentForm()

    
    return render(
    request,
    "lyrics/lyric_detail.html",
    {
        "lyric": lyric,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,

    },
)
