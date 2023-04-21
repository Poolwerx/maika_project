from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect  # Add this
from .models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


# функция (обработчик) главной страницы
def index(request):
    if request.user.is_authenticated:
        user_profile = request.user
    else:
        user_profile = None
    context = {'user_profile': user_profile}
    return render(request, 'main/index.html', context=context)


# функция (обработчик) страницы о сайте
def about(request):
    if request.user.is_authenticated:
        user_profile = request.user
    else:
        user_profile = None
    context = {'user_profile': user_profile}
    return render(request, 'main/about.html', context=context)


# функция (обработчик) страницы регистрации
@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            User.objects.create_user(username=username, email=email, password=password1)
            user = authenticate(request, username=username, password=password1)
            user_profile = UserProfile(user=user)
            user_profile.save()
            if user is not None:
                login(request, user)
                return redirect('index')  # перенаправляем на главную страницу после регистрации
    return render(request, 'main/register.html')


# функция (обработчик) страницы логирования/авторизации пользователя
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('email_text')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'main/login.html')


# функция (обработчик) страницы пользователя
def account_view(request, nickname):
    if request.user.is_authenticated:
        user_profile = request.user
    else:
        user_profile = None
    context = {'user_profile': user_profile,
               'user': None,
               'verification': False}
    try:
        user = User.objects.get(username=nickname)
        if User.objects.get(username=nickname) == request.user:
            context = {'user_profile': user_profile,
                       'user': user,
                       'verification': True}
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'main/accounts.html', context=context)


# функция (обработчик) выхода пользователя из сессии
def logout_view(request):
    logout(request)
    return redirect('index')
