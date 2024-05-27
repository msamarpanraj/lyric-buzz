from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Lyric, Comment
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
        print("Received a POST request")
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
    print("About to render template")

    
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

def comment_edit(request, slug, comment_id):
    """
    view to edit comments
    """
    if request.method == "POST":

        queryset = Lyric.objects.filter(status=1)
        lyric = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.user == request.user:
            comment = comment_form.save(commit=False)
            comment.lyric = lyric
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating comment!')

    return HttpResponseRedirect(reverse('lyric_detail', args=[slug]))

def comment_delete(request, slug, comment_id):
    """
    view to delete comment
    """
    queryset = Lyric.objects.filter(status=1)
    lyric = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.user == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('lyric_detail', args=[slug]))