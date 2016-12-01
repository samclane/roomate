from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CreateUserForm


def index(request):
    if request.user.is_authenticated:
        return HttpResponse("Hello, world. You're at the roomate_app index.")
    else:
        return HttpResponse("Please log in.")


def login_menu(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
    else:
        return HttpResponse("Login failed.")


def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            if username and password:
                u, created = User.objects.get_or_create(username=username)
                if created:
                    # user created
                    u.set_password(password)
                    u.save()
                    return HttpResponseRedirect('/roomate_app/login/')
                # else some error occured
                else:
                    return HttpResponse("Error occurred while making user account.")
    else:
        form = CreateUserForm()

    return render(request, 'registration/create_user.html', {'form': form})

# @login_required(login_url='login/')
# def main(request):
#     pass