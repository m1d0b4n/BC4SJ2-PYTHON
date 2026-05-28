from django.shortcuts import render
from django.db import connection
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import AddBookForm, EditBookForm
from .models import Book
from django.db import IntegrityError, DatabaseError


def books_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM livres")
        books = cursor.fetchall()
    return render(request, 'books.html', {'books': books})



def book_detail_view(request, book_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM livres WHERE id = %s", [book_id])
        book = cursor.fetchone()
    return render(request, 'book_detail.html', {'book': book, 'is_admin': request.session.get('role') == 'admin'})

def delete_book_view(request, book_id):
    if request.session.get('role') == 'admin':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM livres WHERE id = %s", [book_id])
        return redirect('books')
    return HttpResponse("Unauthorized", status=401)

def edit_book_view(request, book_id):
    if request.session.get('role') == 'admin':
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM livres WHERE id = %s", [book_id])
            book = cursor.fetchone()
            if request.method == 'POST':
                form = EditBookForm(request.POST)
                if form.is_valid():
                    try:
                        cursor.execute("UPDATE livres SET titre = %s, auteur = %s, description = %s, date_publication = %s, isbn = %s, photo_url = %s WHERE id = %s", [form.cleaned_data['title'], form.cleaned_data['author'], form.cleaned_data['description'], form.cleaned_data['date_publication'], form.cleaned_data['isbn'], form.cleaned_data['cover'], book_id])
                        return redirect('book_detail', book_id=book_id)
                    except (IntegrityError, DatabaseError) as e:
                        form.add_error(None, "An error occurred while updating the book: {}".format(e))
            else:
                form = EditBookForm(initial={
                    'title': book[1],
                    'author': book[2],
                    'description': book[5],
                    'date_publication': book[3],
                    'isbn': book[4],
                    'cover': book[7],
                })
        return render(request, 'edit_book.html', {'form': form})
    return HttpResponse("Unauthorized", status=401)

def add_book_view(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            book = Book(
                titre=form.cleaned_data['title'],
                auteur=form.cleaned_data['author'],
                description=form.cleaned_data['description'],
                date_publication=form.cleaned_data['date_publication'],
                isbn=form.cleaned_data['isbn'],
                photo_url=form.cleaned_data['cover'],
                statut='disponible')
            
            try:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO livres (titre, auteur, description, date_publication, isbn, photo_url, statut) VALUES (%s, %s, %s, %s, %s, %s, %s)", [book.titre, book.auteur, book.description, book.date_publication, book.isbn, book.photo_url, book.statut])
                return redirect('books')
            except (IntegrityError, DatabaseError) as e:
                form.add_error(None, "An error occurred while adding the book: {}".format(e))
    else:
        form = AddBookForm()
    return render(request, 'add_book.html', {'form': form})