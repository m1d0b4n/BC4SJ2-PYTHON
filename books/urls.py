from django.urls import path
from .views import books_view, book_detail_view, delete_book_view, edit_book_view, add_book_view

urlpatterns = [
    path('', books_view, name='books'),
    path('<int:book_id>/', book_detail_view, name='book_detail'),
    path('<int:book_id>/delete/', delete_book_view, name='delete_book'),
    path('<int:book_id>/edit/', edit_book_view, name='edit_book'),
    path('add/', add_book_view, name='add_book')
]
