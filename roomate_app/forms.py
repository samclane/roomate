from django import  forms

class CreateUserForm(forms.Form):
    userName = forms.CharField(label='Username:', max_length = 100)
    userPass = forms.CharField(label='Password', max_length=100)