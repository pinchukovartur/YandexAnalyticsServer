from django.contrib import auth
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
import os

from .forms import PostForm
from .models import Post


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


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    module_dir = os.path.dirname(__file__).replace("blog", "media")  # get current directory
    file_path = os.path.join(module_dir, str(post.script))
    f = open(file_path, "r")
    script_text = f.read()
    f.close()

    return render(request, 'blog/post_detail.html', {'post': post, "script_text": script_text})


def post_start(request):
    post = get_object_or_404(Post, pk=request.POST.get('post_id', ''))
    print(post.script)
    ## СТАРТ СКРИПТА
    module_dir = os.path.dirname(__file__).replace("blog", "media")  # get current directory
    file_path = os.path.join(module_dir, str(post.script))
    f = open(file_path, "r")
    script_text = f.read()
    f.close()

    return render(request, 'blog/post_detail.html', {'post': post, "script_text": script_text})