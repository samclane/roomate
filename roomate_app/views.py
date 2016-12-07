from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CreateUserForm, CreateBillForm, CreateGroceryForm, CreateChoreForm
from .models import Bill, Grocery, Chore
from django.db.models import Sum


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


def view_chores(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateChoreForm(request.POST)
            if form.is_valid():
                c = Chore.objects.create(**form.cleaned_data)
                c.save()
                return HttpResponseRedirect('view_chores')
        else:
            form = CreateChoreForm()
        chore_list = Chore.objects.exclude(if_complete=True).order_by('-due_date')[:]
        return render(request, 'ViewChores.html', {'form': form, 'chore_list': chore_list})
    else:
        return HttpResponse("Please log in.")


def view_grocery(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateGroceryForm(request.POST)
            if form.is_valid():
                g = Grocery.objects.create(**form.cleaned_data)
                g.remaining_cost = g.total_cost
                g.save()
                return HttpResponseRedirect('view_grocery')
        else:
            form = CreateGroceryForm()
        grocery_list = Grocery.objects.exclude(remaining_cost=0).exclude(if_purchased=True).order_by('-store')[:]
        return render(request, 'ViewGrocery.html', {'form': form, 'grocery_list': grocery_list})
    else:
        return HttpResponse("Please log in.")


def view_expense_report(request):
    if request.user.is_authenticated:
        grocery_list = Grocery.objects.filter(if_purchased=True).order_by('-store')[:]
        grocery_sum = grocery_list.aggregate(Sum('remaining_cost')).values()[0]
        bill_list = Bill.objects.filter(if_paid=True).order_by('-due_date')[:]
        bill_sum = bill_list.aggregate(Sum('remaining_cost')).values()[0]
        return render(request, 'ViewExpenseReport.html',
                      {'grocery_list': grocery_list, 'grocery_sum': grocery_sum, 'bill_list': bill_list,
                       'bill_sum': bill_sum})
    else:
        return HttpResponse("Please log in.")


def view_duty_report(request):
    if request.user.is_authenticated:
        grocery_list = Grocery.objects.filter(if_purchased=False).order_by('-store')[:]
        grocery_sum = grocery_list.aggregate(Sum('remaining_cost')).values()[0]
        chore_list = Chore.objects.filter(if_complete=False).order_by('-due_date')[:]
        bill_list = Bill.objects.filter(if_paid=False).order_by('-due_date')[:]
        bill_sum = bill_list.aggregate(Sum('remaining_cost')).values()[0]
        return render(request, 'ViewDutyReport.html',
                      {'grocery_list': grocery_list, 'grocery_sum': grocery_sum, 'bill_list': bill_list,
                       'bill_sum': bill_sum})
    else:
        return HttpResponse("Please log in.")