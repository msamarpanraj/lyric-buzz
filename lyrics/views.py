from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Lyric


# Create your views here.

class LyricList(generic.ListView):
     queryset = Lyric.objects.filter(status=1)
     template_name = "lyrics/index.html"
     paginate_by = 6


def lyric_detail(request, slug):
    """
    Display an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.

    **Template:**

    :template:`blog/post_detail.html`
    """

    queryset = Lyric.objects.filter(status=1)
    lyric = get_object_or_404(queryset, slug=slug)

    return render(
        request,
        "lyrics/lyric_detail.html",
        {"lyric": lyric},
    )
