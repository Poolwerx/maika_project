from django.urls import path, re_path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('register', views.register, name="register"),
    path('login', views.login_page, name="login"),
    path('account/<str:nickname>/', views.account_view, name='account')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
