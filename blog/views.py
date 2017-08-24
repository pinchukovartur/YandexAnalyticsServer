import os
from datetime import datetime

from django.contrib import auth
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .forms import PostForm
from .models import Post
from .scripts_controller.scripts_controller import run_script, stop_scripts, get_script_status


def post_list(request):
    if request.user.is_authenticated():
        posts = Post.objects.filter()
        # если это не админ, то отдаем только пользовательские скрипты
        if not auth.get_user(request).is_superuser:
            res_posts = list()
            for post in posts:
                if str(post.author) == str(auth.get_user(request).username):
                    res_posts.append(post)
            posts = res_posts

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

    if str(post.author) != str(auth.get_user(request).username) and auth.get_user(request).is_superuser is False:
        raise NameError("Ошибка доступа!!!")
    script_text = ""
    if str(post.script) is not "":
        module_dir = os.path.dirname(__file__) + "/scripts_controller/"
        file_path = os.path.join(module_dir, str(post.script))
        f = open(file_path, "rb")
        script_text = f.read().decode("UTF-8")
        f.close()

    # if folder with user log not exist create her
    if not os.path.isdir(os.path.dirname(__file__) + "\\scripts_controller\\logs\\" + str(post.author) + "\\"):
        os.mkdir(os.path.dirname(__file__) + "\\scripts_controller\\logs\\" + str(post.author))

    list_logs = os.listdir(os.path.dirname(__file__) + "\\scripts_controller\\logs\\" + str(post.author) + "\\")

    script_logs = list()
    for log in list_logs:
        if log.endswith(str(post.title).replace(" ", "") + ".txt"):
            script_logs.append(log)

    status = get_script_status(str(post.author), str(post.title))

    return render(request, 'blog/post_detail.html',
                  {'post': post, "script_text": script_text, "script_logs": script_logs, "status": status})


def post_start(request):
    post = get_object_or_404(Post, pk=request.POST.get('post_id', ''))

    if str(post.author) != str(auth.get_user(request).username):
        raise NameError("Ошибка доступа!!!")

    if str(post.script) != "":
        module_dir = os.path.dirname(__file__) + "/scripts_controller/"
        file_path = os.path.join(module_dir, str(post.script))

        run_script(str(post.title), str(post.type), str(post.author), file_path, str(datetime.today()))

    return redirect('post_detail', request.POST.get('post_id', ''))


def model_form_upload(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        post = form.save(commit=False)
        post.author = request.user
        post.published_date = timezone.now()
        post.save()
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_stop(request):
    post = get_object_or_404(Post, pk=request.POST.get('post_id', ''))

    if str(post.author) != str(auth.get_user(request).username):
        raise NameError("Ошибка доступа!!!")

    stop_scripts(str(post.author), str(post.title))

    return redirect('post_detail', request.POST.get('post_id', ''))


def post_delete(request):
    posts = Post.objects.filter(pk=request.POST.get('post_id', ''))
    for post in posts:
        stop_scripts(str(post.author), str(post.title))
        if str(post.script) != "":
            script_dir = os.path.dirname(__file__) + "/scripts_controller/" + str(post.script)
            os.remove(script_dir)
        post.delete()
    return HttpResponseRedirect('/')


def post_update(request):
    if request.method == "POST":
        Post.objects.filter(pk=request.POST.get('post_id', '')).delete()
        form = PostForm(request.POST, request.FILES)
        post = form.save(commit=False)
        post.pk = request.POST.get('post_id', '')
        post.author = request.user
        post.published_date = timezone.now()
        post.save()
        if form.is_valid():
            form.save()
            return redirect('post_detail', request.POST.get('post_id', ''))
    else:
        post = get_object_or_404(Post, pk=request.GET.get('post_id', ''))
        form = PostForm()
        form.fields["title"].initial = post.title
        form.fields["type"].initial = post.type
        form.fields["text"].initial = post.text
        form.fields["script"].inital = post.script
        return render(request, 'blog/post_update.html', {"form": form, "post": post})


def post_start_insert_in_db(request):
    print("hello")
    script_code = ""
    if script_code == 'start_download':
        pass
        # check_script_status()
        # stop_start_new_script()
    elif script_code == "download_ok":
        pass
        # activate_start_new_script()
    else:
        return HttpResponse("return this string")
