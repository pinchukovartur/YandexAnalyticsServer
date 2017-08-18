from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect
from .forms import PostForm
from .models import Post
from django.contrib import auth


def post_list(request):
    if request.user.is_authenticated():
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        return render(request, 'blog/post_list.html', {'posts': posts, 'username': auth.get_user(request).username})
    else:
        return render(request, 'blog/post_list.html')


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
