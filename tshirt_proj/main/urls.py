from django.urls import path, re_path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('register', views.register, name="register"),
    path('login', views.login_page, name="login"),
    path('account/<str:nickname>/change_profile', views.account_view_change_profile, name="change"),
    path('account/<str:nickname>/add_new_item', views.account_view_add_new_item, name="additem"),
    path('account/<str:nickname>/', views.account_view, name='account'),
    path('item/<str:author>/<int:id>/', views.item_check, name='item_check'),
    path('item/', views.item_catalog, name='item_catalog'),
    path('logout', views.logout_view, name="logout")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
