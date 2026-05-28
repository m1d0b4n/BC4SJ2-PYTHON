# myproject/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Email ou mot de passe incorrect')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def books_view(request):
    return render(request, 'books.html')

@login_required
def home_view(request):
    return render(request, 'home.html')
