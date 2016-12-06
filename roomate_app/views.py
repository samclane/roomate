from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CreateUserForm, CreateBillForm
from .models import Bill, Grocery, Chore


def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
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


def view_bills(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateBillForm(request.POST)
            if form.is_valid():
                b = Bill.objects.create(**form.cleaned_data)
                b.remaining_cost = b.total_cost
                b.save()
                return HttpResponseRedirect('view_bills')
        else:
            form = CreateBillForm()
        bill_list = Bill.objects.exclude(remaining_cost=0).order_by('-due_date')[:]
        return render(request, 'ViewBills.html', {'form': form, 'bill_list': bill_list})
    else:
        return HttpResponse("Please log in.")

# @login_required(login_url='login/')
# def main(request):
#     pass
