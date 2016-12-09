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
import logging


def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html', {'username': str(request.user.username)})
    else:
        return HttpResponseRedirect('/roomate_app/login/')


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
                b, created = Bill.objects.get_or_create(**form.cleaned_data)
                if created:
                    b.remaining_cost = b.total_cost
                b.save()
                return HttpResponseRedirect('view_bills')
        else:
            if len(request.GET) != 0:
                if (str(request.GET.values()[0]) == "Edit"):
                    b_instance = Bill.objects.all().get(id=int(request.GET.keys()[0]))
                    form = CreateBillForm(instance=b_instance)
                    b_instance.delete()
            else:
                form = CreateBillForm()
        bill_list = Bill.objects.exclude(remaining_cost=0).exclude(if_paid=True).order_by('-due_date')[:]
        return render(request, 'ViewBills.html', {'form': form, 'bill_list': bill_list})
    else:
        return HttpResponseRedirect('/roomate_app/login/')


def view_chores(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateChoreForm(request.POST)
            if form.is_valid():
                c, created = Chore.objects.get_or_create(**form.cleaned_data)
                c.save()
                return HttpResponseRedirect('view_chores')
        else:
            if len(request.GET) != 0:
                if(str(request.GET.values()[0]) == "Edit"):
                    c_instance = Chore.objects.all().get(id=int(request.GET.keys()[0]))
                    form = CreateChoreForm(instance=c_instance)
                    c_instance.delete()
            else:
                form = CreateChoreForm()
        chore_list = Chore.objects.exclude(if_complete=True).order_by('-due_date')[:]
        return render(request, 'ViewChores.html', {'form': form, 'chore_list': chore_list})
    else:
        return HttpResponseRedirect('/roomate_app/login/')


def view_grocery(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateGroceryForm(request.POST)
            if form.is_valid():
                g, created = Grocery.objects.get_or_create(**form.cleaned_data)
                if created:
                    g.remaining_cost = g.total_cost
                g.save()
                return HttpResponseRedirect('view_grocery')
        else:
            if len(request.GET) != 0:
                if(str(request.GET.values()[0]) == "Edit"):
                    g_instance = Grocery.objects.all().get(id=int(request.GET.keys()[0]))
                    form = CreateGroceryForm(instance=g_instance)
                    g_instance.delete()
            else:
                form = CreateGroceryForm()
        grocery_list = Grocery.objects.exclude(remaining_cost=0).exclude(if_purchased=True).order_by('-store')[:]
        return render(request, 'ViewGrocery.html', {'form': form, 'grocery_list': grocery_list})
    else:
        return HttpResponseRedirect('/roomate_app/login/')


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
        return HttpResponseRedirect('/roomate_app/login/')


def view_duty_report(request):
    if request.user.is_authenticated:
        grocery_list = Grocery.objects.filter(if_purchased=False).exclude(remaining_cost=0).order_by('-store')[:]
        grocery_sum = grocery_list.aggregate(Sum('remaining_cost')).values()[0]
        chore_list = Chore.objects.filter(if_complete=False).filter(assignee__username=str(request.user.username)).order_by('-due_date')[:]
        bill_list = Bill.objects.filter(if_paid=False).exclude(remaining_cost=0).order_by('-due_date')[:]
        bill_sum = bill_list.aggregate(Sum('remaining_cost')).values()[0]
        return render(request, 'ViewDutyReport.html',
                      {'grocery_list': grocery_list, 'grocery_sum': grocery_sum, 'bill_list': bill_list,
                       'bill_sum': bill_sum, 'chore_list':chore_list})
    else:
        return HttpResponseRedirect('/roomate_app/login/')
