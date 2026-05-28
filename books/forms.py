from django import forms
from django import forms
from .models import Book

class AddBookForm(forms.Form):
    title = forms.CharField(label='Titre', max_length=100, required=True)
    author = forms.CharField(label='Auteur', max_length=100, required=True)
    description = forms.CharField(label='Description', widget=forms.Textarea, required=True)
    date_publication = forms.DateField(label='Date de Publication', required=True)
    isbn = forms.CharField(label='ISBN', max_length=13, required=True)
    cover = forms.URLField(label='URL de l\'image', required=True)
    
    

class EditBookForm(forms.Form):
    title = forms.CharField(label='Titre', max_length=100, required=True)
    author = forms.CharField(label='Auteur', max_length=100, required=True)
    description = forms.CharField(label='Description', widget=forms.Textarea, required=True)
    date_publication = forms.DateField(label='Date de Publication', required=True)
    isbn = forms.CharField(label='ISBN', max_length=13, required=True)
    cover = forms.URLField(label='URL de l\'image', required=True)