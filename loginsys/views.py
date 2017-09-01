from django.contrib import auth
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect, render


@csrf_protect
def login(request):
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            login_error = "Пользователь не найден"
            return render(request, 'blog/post_list.html', {"login_error": login_error})
    else:
        raise NameError("Ошибка, не известный запрос")


def logout(request):
    auth.logout(request)
    return redirect("/")
