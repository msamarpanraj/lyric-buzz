from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Lyric, Comment, Profile
from .forms import CommentForm
from .forms import LyricSearchForm
from .forms import LyricSubmissionForm
from .forms import ProfileForm
from django.core.paginator import Paginator



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


def search_lyrics(request):
    form = LyricSearchForm()
    q = ''
    results = []
   
    if 'q' in request.GET:
        form = LyricSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            results = Lyric.objects.filter(song_name__icontains=q)

    return render(request, 'lyrics/search_results.html',
                  {'form': form,
                   'q': q,
                   'results': results})


class AllLyricsList(generic.ListView):
    queryset = Lyric.objects.filter(status=1)
    template_name = "lyrics/all_lyrics.html"
    context_object_name = 'lyric_list'
    paginate_by = 5


@login_required
def submit_lyric(request):
    if request.method == "POST":
        form = LyricSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            lyric = form.save(commit=False)
            lyric.user = request.user
            lyric.status = 2  
            lyric.is_approved = False  
            lyric.save()
            messages.success(request, "Your lyric has been submitted and is awaiting approval.")
            return redirect('home')
    else:
        form = LyricSubmissionForm()
    return render(request, 'lyrics/submit_lyric.html', {'form': form})


@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)

    lyrics = Lyric.objects.filter(user=request.user)
    paginator = Paginator(lyrics, 10)  # Show 10 lyrics per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'lyrics/profile.html', {'form': form, 'page_obj': page_obj})

@login_required
def edit_lyric(request, slug):
    lyric = get_object_or_404(Lyric, slug=slug, user=request.user)
    if request.method == "POST":
        form = LyricSubmissionForm(request.POST, request.FILES, instance=lyric)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your lyric has been updated.')
            return redirect('profile')
    else:
        form = LyricSubmissionForm(instance=lyric)
    return render(request, 'lyrics/edit_lyric.html', {'form': form, 'lyric': lyric})

@login_required
def delete_lyric(request, slug):
    lyric = get_object_or_404(Lyric, slug=slug, user=request.user)
    if request.method == "POST":
        lyric.delete()
        messages.success(request, 'Your lyric has been deleted.')
        return redirect('profile')
    return render(request, 'lyrics/confirm_delete_lyric.html', {'lyric': lyric})
    
@login_required
def like_lyric(request, slug):
    lyric = get_object_or_404(Lyric, slug=slug)
    if lyric.likes.filter(id=request.user.id).exists():
        lyric.likes.remove(request.user)
        messages.success(request, 'You haved unliked this lyric.')

    else:
        lyric.likes.add(request.user)
        messages.success(request, 'You haved liked this lyric.')

    return redirect('lyric_detail', slug=slug)