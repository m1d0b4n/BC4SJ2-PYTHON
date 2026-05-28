from django.shortcuts import render
from django.db import connection

def home_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(id) FROM livres")
        books_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(id) FROM utilisateurs")
        users_count = cursor.fetchone()[0]
    
    context = {
        'books_count': books_count,
        'users_count': users_count,
    }
    
    return render(request, 'home.html', context)
