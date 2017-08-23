import os
from datetime import datetime

from django.contrib import auth
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponseRedirect
from .forms import PostForm
from .models import Post
from .scripts_controller.scripts_controller import run_script, stop_scripts


def post_list(request):
    if request.user.is_authenticated():
        posts = Post.objects.filter()
        # hand filter))
        res_posts = list()
        for post in posts:
            if str(post.author) == str(auth.get_user(request).username):
                res_posts.append(post)

        return render(request, 'blog/post_list.html', {'posts': res_posts, 'username': auth.get_user(request).username})
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

    if str(post.author) != str(auth.get_user(request).username):
        raise NameError("Ошибка доступа!!!")

    module_dir = os.path.dirname(__file__) + "/scripts_controller/"
    file_path = os.path.join(module_dir, str(post.script))
    f = open(file_path, "r")
    script_text = f.read()
    f.close()

    # if folder with user log not exist create her
    if not os.path.isdir(os.path.dirname(__file__) + "\\scripts_controller\\logs\\" + str(post.author) + "\\"):
        os.mkdir(os.path.dirname(__file__) + "\\scripts_controller\\logs\\" + str(post.author))

    list_logs = os.listdir(os.path.dirname(__file__) + "\\scripts_controller\\logs\\" + str(post.author) + "\\")

    script_logs = list()
    for log in list_logs:
        if log.endswith(str(post.title) + ".txt"):
            script_logs.append(log)

    return render(request, 'blog/post_detail.html',
                  {'post': post, "script_text": script_text, "script_logs": script_logs})


def post_start(request):
    post = get_object_or_404(Post, pk=request.POST.get('post_id', ''))

    if str(post.author) != str(auth.get_user(request).username):
        raise NameError("Ошибка доступа!!!")

    module_dir = os.path.dirname(__file__) + "/scripts_controller/"
    file_path = os.path.join(module_dir, str(post.script))

    run_script(str(post.title), str(post.type), str(post.author), file_path, str(datetime.today()))

    f = open(file_path, "r")
    script_text = f.read()
    f.close()

    return redirect('post_detail', request.POST.get('post_id', ''))


def model_form_upload(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = PostForm()
    return render(request, 'upload.html', {'form': form})


def post_stop(request):
    post = get_object_or_404(Post, pk=request.POST.get('post_id', ''))

    if str(post.author) != str(auth.get_user(request).username):
        raise NameError("Ошибка доступа!!!")

    stop_scripts(str(post.author), str(post.title))

    return redirect('post_detail', request.POST.get('post_id', ''))
