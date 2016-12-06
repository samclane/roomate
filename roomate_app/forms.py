from django import forms
from django.forms import ModelForm
from roomate_app.models import Bill, Grocery, Chore


class CreateUserForm(forms.Form):
    username = forms.CharField(label='username:', max_length=100)
    password = forms.CharField(label='password', max_length=100)


class CreateBillForm(ModelForm):
    class Meta:
        model = Bill
        fields = ['bname', 'company', 'if_purchased', 'due_date', 'total_cost']
        		
class CreateChoreForm(ModelForm):
    class Meta:
        model = Chore
        fields = ['name', 'assignee', 'if_complete', 'due_date', 'total_cost']
		
class CreateGroceryForm(ModelForm):
    class Meta:
        model = Grocery
        fields = ['gname', 'store', 'if_purchased', 'total_cost']
