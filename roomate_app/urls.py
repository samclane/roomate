from django.conf.urls import url

from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', auth_views.login, name='login'),
    url(r'^logout/', auth_views.logout, {'next_page': '/roomate_app'}, name='logout'),
    url(r'^create_user/', views.create_user, name='create_user'),
    url(r'^view_bills/', views.view_bills, name='view_bills'),
    url(r'^view_grocery/', views.view_grocery, name='view_grocery'),
    url(r'^view_chores/', views.view_chores, name='view_chores'),
]
