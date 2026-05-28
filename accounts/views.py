from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth.hashers import check_password
from django.middleware.csrf import get_token
from django.contrib.auth.hashers import make_password

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, mot_de_passe, prenom, role FROM utilisateurs WHERE email = %s", [email])
                user = cursor.fetchone()
            if user is not None and check_password(password, user[1]):
                request.session['is_authenticated'] = True
                request.session['user_id'] = user[0]
                request.session['username'] = user[2]
                request.session['role'] = user[3]
                request.session['is_admin'] = user[3] == 'admin'
                request.session['csrf_token'] = get_token(request)
                return redirect('home')

            else:
                messages.error(request, 'Email ou mot de passe incorrect')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    request.session.flush()
    return redirect('home')

def profile_view(request):
    if(not request.session.get('is_authenticated', False)):
        return redirect('login')

    with connection.cursor() as cursor:
        cursor.execute("SELECT prenom, nom, email FROM utilisateurs WHERE id = %s", [request.session['user_id']])
        user = cursor.fetchone()
    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)


def register_view(request):
    if request.method == 'POST':
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        email = request.POST['email']
        password = request.POST['password']
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM utilisateurs WHERE email = %s", [email])
            user = cursor.fetchone()
        if user is not None:
            error = "Cet email est déjà utilisé."
            return render(request, 'register.html', {'error': error})

        hashed_password = make_password(password)
        
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO utilisateurs (prenom, nom, email, mot_de_passe) VALUES (%s, %s, %s, %s)", [prenom, nom, email, hashed_password])
        return redirect('login')

    return render(request, 'register.html')

def edit_profile(request):
    if request.method == 'POST':
        new_name = request.POST['new_name']
        new_email = request.POST['new_email']

        with connection.cursor() as cursor:
            cursor.execute("SELECT prenom FROM utilisateurs WHERE email = %s", [new_email])
            user = cursor.fetchone()
        if user is not None and user[0] != request.session['username']:
            error = "Cet email est déjà utilisé."
            return render(request, 'edit_profile.html', {'error': error})

        with connection.cursor() as cursor:
            cursor.execute("UPDATE utilisateurs SET prenom = %s, email = %s WHERE id = %s", [new_name, new_email, request.session['user_id']])

        # Redirect the user to their updated profile
        return redirect('profile')

    return render(request, 'edit_profile.html')