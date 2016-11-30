from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CreateUserForm


def index(request):
    if request.user.is_authenticated:
        return HttpResponse("Hello, world. You're at the roomate_app index.")
    else:
        return HttpResponse("Please log in.")


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse("Login successful.")
    else:
        return HttpResponse("Login failed.")


def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = request.POST['userName']
            password = request.POST['userPass']
            if username and password:
                u, created = User.objects.get_or_create(username = username)
                if created:
                    # user created
                    u.set_password(password)
                # else some error occured
    else:
        form = CreateUserForm()

    return render(request, 'registration/create_user.html', {'form': form})

