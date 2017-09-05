import os
from datetime import datetime

import psutil
from django.contrib import auth
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .forms import PostForm
from .models import Post
from .scripts_controller.scripts_controller import run_script, stop_scripts, get_script_status, get_count_script_instance

# статус, когда запускается скрипт обновления БД
DOWNLOAD_STATUS = False


# the method return user script
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


# the method return script information
def post_detail(request, pk):
    # get scrip and his status
    post = get_object_or_404(Post, pk=pk)
    status = get_script_status(str(post.author), str(post.title))
    # if auth script not users and not admin => error
    if str(post.author) != str(auth.get_user(request).username) and auth.get_user(request).is_superuser is False:
        raise NameError("Ошибка доступа!!!")
    script_text = ""
    # if script text not null read text
    if str(post.script) is not "":
        module_dir = os.path.dirname(__file__) + "/scripts_controller/"
        file_path = os.path.join(module_dir, str(post.script))
        f = open(file_path, "rb")
        script_text = f.read().decode("UTF-8")
        f.close()
    # if folder with user log not exist create her
    if not os.path.isdir(os.path.dirname(__file__) + "/scripts_controller/logs/" + str(post.author) + "/"):
        os.mkdir(os.path.dirname(__file__) + "/scripts_controller/logs/" + str(post.author))
    # read log files
    list_logs = os.listdir(os.path.dirname(__file__) + "/scripts_controller/logs/" + str(post.author) + "/")
    script_logs = list()
    for log in list_logs:
        if log.endswith("%"+str(post.title).replace(" ", "") + "%.txt"):
            script_logs.append(log)
    # get count instance
    count_instance = get_count_script_instance(str(post.author), str(post.title))
    # return response
    return render(request, 'blog/post_detail.html',
                  {'post': post, "script_text": script_text, "script_logs": script_logs, "status": status,
                   "count_instance": count_instance})


# the method run script
def post_start(request):
    # if database do not update
    if not DOWNLOAD_STATUS:
        # get post
        post = get_object_or_404(Post, pk=request.POST.get('post_id', ''))
        # if script auth not user or admin => error
        if str(post.author) != str(auth.get_user(request).username) and auth.get_user(request).is_superuser is False:
            raise NameError("Ошибка доступа!!!")
        # if script not empty run his
        if str(post.script) != "":
            module_dir = os.path.dirname(__file__) + "/scripts_controller/"
            file_path = os.path.join(module_dir, str(post.script))
            run_script(str(post.title), str(post.type), str(post.author), file_path, str(datetime.today()))
        # return script information
        return redirect('post_detail', request.POST.get('post_id', ''))
    else:
        return HttpResponse("Sorry! but the database is scheduled to be updated, we can not run a new script. Please "
                            "wait...")


# the method add new script
def model_form_upload(request):
    # if auth anonymous => error
    print(111111)
    if auth.get_user(request).is_anonymous:
        raise NameError("Ошибка! авторизуйтесь для добавления нового скрипта")
    # if POST add script
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if __check_name_script(request.POST.get('title', '')):
            form = PostForm()
            return render(request, 'blog/post_edit.html', {'form': form, "name_error": "This name is already taken"})
        post = form.save(commit=False)
        post.author = request.user
        post.published_date = timezone.now()
        post.save()
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect('/')
    # if GET return form
    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})


# the method stop script
def post_stop(request):
    # get object
    post = get_object_or_404(Post, pk=request.POST.get('post_id', ''))
    # if auth script != user and user != admin = error
    if str(post.author) != str(auth.get_user(request).username) and auth.get_user(request).is_superuser is False:
        raise NameError("Ошибка доступа!!!")
    # stop script
    stop_scripts(str(post.author), str(post.title))
    # return script information
    return redirect('post_detail', request.POST.get('post_id', ''))


# the method delete script
def post_delete(request):
    # get script
    posts = Post.objects.filter(pk=request.POST.get('post_id', ''))
    for post in posts:
        # stop script
        stop_scripts(str(post.author), str(post.title))
        # if script code not null
        if str(post.script) != "":
            # delete script file
            script_dir = os.path.dirname(__file__) + "/scripts_controller/" + str(post.script)
            os.remove(script_dir)
        # delete from db
        post.delete()
        # delete log files
        list_logs = os.listdir(os.path.dirname(__file__) + "/scripts_controller/logs/" + str(post.author) + "/")
        for log in list_logs:
            if log.endswith("%" + str(post.title).replace(" ", "") + "%.txt"):
                os.remove(os.path.dirname(__file__) + "/scripts_controller/logs/" + str(post.author) + "/" + log)
    return HttpResponseRedirect('/')


# the method update script
def post_update(request):
    if request.method == "POST":
        # get object
        post = get_object_or_404(Post, pk=request.POST.get('post_id', ''))
        # check of the same name
        if __check_name_script(post.title) and request.POST.get('title', '') != post.title:
            form = PostForm()
            form.fields["title"].initial = post.title
            form.fields["type"].initial = post.type
            form.fields["text"].initial = post.text
            form.fields["script"].inital = post.script
            return render(request, 'blog/post_update.html', {"form": form, "post": post, "name_error": "This name is already taken"})
        # if auth script != user and user != admin = error
        if str(post.author) != str(auth.get_user(request).username) and auth.get_user(request).is_superuser is False:
            raise NameError("Ошибка доступа!!!")
        # get from and create new script
        form = PostForm(request.POST, request.FILES)
        post = form.save(commit=False)
        post.pk = request.POST.get('post_id', '')
        post.author = request.user
        post.published_date = timezone.now()
        # if file = null => old script text = new script text
        if len(request.FILES) == 0:
            post.script = get_object_or_404(Post, pk=request.POST.get('post_id', '')).script
        # if all good save script and delete old
        if form.is_valid():
            Post.objects.filter(pk=request.POST.get('post_id', '')).delete()
            form.save()
            post.save()
            return redirect('post_detail', request.POST.get('post_id', ''))
    else:
        # if GET return form
        post = get_object_or_404(Post, pk=request.GET.get('post_id', ''))
        form = PostForm()
        form.fields["title"].initial = post.title
        form.fields["type"].initial = post.type
        form.fields["text"].initial = post.text
        form.fields["script"].inital = post.script
        return render(request, 'blog/post_update.html', {"form": form, "post": post})


# the method get update status
def post_start_insert_in_db(status_code):
    script_code = status_code
    global DOWNLOAD_STATUS
    if str(script_code) == 'start':
        DOWNLOAD_STATUS = True
        if __check_run_script():
            return HttpResponse("you can not download")
        else:
            return HttpResponse("you can download")
    elif script_code == "ok":
        DOWNLOAD_STATUS = False
        return HttpResponse("okay")
    else:
        return HttpResponse("understand script_code")


# метод проверят есть ли хоть один активный скрипт в даный момент
def __check_run_script():
    posts = Post.objects.filter()
    for post in posts:
        if get_script_status(str(post.author), str(post.title)):
            return True
    return False


# the method check name scripts in db
def __check_name_script(name):
    posts = Post.objects.filter()
    for post in posts:
        if post.title == name:
            return True
    return False


def __check_user(post, request):
    if str(post.author) != request.user.is_authenticated:
        return HttpResponse("Access closed")


def delete_logs_files(post):
    # read log files
    list_logs = os.listdir(os.path.dirname(__file__) + "/scripts_controller/logs/" + str(post.author) + "/")
    script_logs = list()
    for log in list_logs:
        if log.endswith("%" + str(post.title).replace(" ", "") + "%.txt"):
            print(log)


# js method
def get_cpu_info():
    return HttpResponse(psutil.cpu_percent(interval=1))
def get_memory_info():
    return HttpResponse(psutil.virtual_memory().percent)
def get_disk_info():
    return HttpResponse(psutil.disk_usage('/').percent)
