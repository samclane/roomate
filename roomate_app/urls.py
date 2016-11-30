from django.conf.urls import url

from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', auth_views.login, name='login'),
    url(r'^logout/', auth_views.logout, {'next_page': '/roomate_app'}, name='logout'),
    url(r'^create_user/', views.create_user, name='create_user'),
]