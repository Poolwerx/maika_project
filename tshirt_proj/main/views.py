from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect  # Add this
from .models import UserProfile, Image, UserItems
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseForbidden
from django.core.files.storage import FileSystemStorage
from django.conf import settings


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
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            User.objects.create_user(username=username, email=email, password=password1)
            user = authenticate(request, username=username, password=password1)
            user_profile = UserProfile(user=user, user_name=user.username)
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
@login_required
def account_view(request, nickname):
    try:
        if request.user.is_authenticated:
            user_profile = request.user
        else:
            user_profile = None
        user = UserProfile.objects.get(user_name=nickname)
        user_items = UserItems.objects.filter(author=nickname).all()
        context = {'user_profile': user_profile,
                   'user': user,
                   'user_items': user_items}
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'main/accounts.html', context=context)


# функция (обработчик) изменения данных о странице пользователя
@login_required
def account_view_change_profile(request, nickname):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user_name=nickname)
        user = User.objects.get(username=nickname)
        if request.POST.get('checkbox'):
            user_profile.verified_account = True
        if request.FILES:
            user_profile_obj = UserProfile.objects.all()
            file = request.FILES['logo']
            file.name = f"{user.username}_user_profile{user.id}{len(user_profile_obj)}.{file.name.split('.')[1]}"
            fs = FileSystemStorage(location='main/static/user_profiles/')
            filename = fs.save(file.name, file)
            file_url = fs.url(filename)
            user_profile.profile_picture = file_url
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('second_name')
        user_profile.about = request.POST.get('text_about')
        user_profile.save()
        user.save()
        return redirect('index')
    try:
        if request.user.is_authenticated:
            user_profile = request.user
        else:
            user_profile = None
        user = UserProfile.objects.get(user_name=nickname)
        context = {'user_profile': user_profile,
                   'user': user}
        if user_profile.username != user.user_name:
            return HttpResponseForbidden()
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'main/change_profile.html', context=context)


# тут прописать user_item_save + редирект + просмотреть правильно ли все созхраняется
@login_required
def account_view_add_new_item(request, nickname):
    if request.method == "POST":
        user_item = UserItems.objects.create(author=nickname, item_name=request.POST.get('item_name'),
                                             description=request.POST.get('text_about'))
        if request.POST.get('category1'):
            user_item.category = 'Классика'
        elif request.POST.get('category2'):
            user_item.category = 'Спорт'
        elif request.POST.get('category3'):
            user_item.category = 'Лонгслив'
        elif request.POST.get('category5'):
            user_item.category = 'Кастом'
        if request.FILES:
            user_profile_obj = UserItems.objects.all()
            file = request.FILES['main_picture']
            file.name = f"main_item_picture{len(user_profile_obj)}.{file.name.split('.')[1]}"
            fs = FileSystemStorage(location='main/static/user_profiles/')
            filename = fs.save(file.name, file)
            image_main, image_dop1, image_dop2 = None, None, None
            image_main = fs.url(filename)
            if request.FILES['dop1_picture']:
                file = request.FILES['dop1_picture']
                file.name = f"dop1_item_picture{len(user_profile_obj)}.{file.name.split('.')[1]}"
                fs = FileSystemStorage(location='main/static/user_profiles/')
                filename = fs.save(file.name, file)
                image_dop1 = fs.url(filename)
            if request.FILES['dop2_picture']:
                file = request.FILES['dop2_picture']
                file.name = f"dop2_item_picture{len(user_profile_obj)}.{file.name.split('.')[1]}"
                fs = FileSystemStorage(location='main/static/user_profiles/')
                filename = fs.save(file.name, file)
                image_dop2 = fs.url(filename)
            image_item = Image.objects.create(image_main=image_main, image_dop1=image_dop1, image_dop2=image_dop2)
            user_item.pictures = image_item
        user_item.save()
    try:
        if request.user.is_authenticated:
            user_profile = request.user
        else:
            user_profile = None
        user = UserProfile.objects.get(user_name=nickname)
        context = {'user_profile': user_profile,
                   'user': user}
        if user_profile.username != user.user_name:
            return HttpResponseForbidden()
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'main/add_new_item.html', context=context)


# функция (обработчик) выхода пользователя из сессии
def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def item_check(request, author, id):
    try:
        if request.user.is_authenticated:
            user_profile = request.user
        else:
            user_profile = None
        user = UserProfile.objects.get(user_name=author)
        user_items = UserItems.objects.filter(author=author, id=id).all()
        context = {'user_profile': user_profile,
                   'user': user,
                   'user_items': user_items}
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'main/item_check.html', context=context)


@login_required
def item_catalog(request):
    try:
        if request.user.is_authenticated:
            user_profile = request.user
        else:
            user_profile = None
        user_items = UserItems.objects.filter().all()
        context = {'user_profile': user_profile,
                   'user_items': user_items}
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'main/item_catalog.html', context=context)
