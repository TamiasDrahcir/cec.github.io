from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from register.models import User
from register.forms import RegisterForm, LoginForm


def register(response):
    print("Start Signin!")
    if response.method == "POST":
        form = RegisterForm(response.POST)
        print(form.is_valid())
        print(form.cleaned_data)
        search_string = '<input type="text" name="username" value="'
        chunk1 = str(form)[str(form).find(search_string)+len(search_string):]
        name = chunk1[:chunk1.find('"')]
        new_user = User.objects.create(username=name,
                        house=form.cleaned_data['house'],
                        account_type=form.cleaned_data['account_type'],
                        password=form.cleaned_data['password1'])            
        return redirect("http://127.0.0.1:8000/carbon_emissions_calculator/login/")
    else:
        form = RegisterForm()
    return render(response,"register/register.html",{"form":form})

def Login_cec(response):
    if response.method == 'POST':
        form = LoginForm(data=response.POST)
        user_data = form.data
        username = user_data['username']
        password = user_data['password']
        account = user_data['account']
    
        print("Username:",username)
        print("Password:",password)
        print("Account: ", account)
        print("Data Extracted")
        filtered_user = User.objects.filter(username=username)
        if len(filtered_user) == 1:
            if filtered_user[0].password == password and filtered_user[0].account_type == account:
                login(response,filtered_user[0])
                print("Login Successful!!!")
                return redirect("http://127.0.0.1:8000/carbon_emissions_calculator/home/")
            else:
                print("Incorrect credentials")
                print(filtered_user[0])
        else:
            print("No such user")
    else:
        form = LoginForm()
    return render(response, "cec/login.html", {"form":form})