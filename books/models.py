from django.db import models

class Book():
    titre = models.CharField(max_length=100) 
    auteur = models.CharField(max_length=100)
    date_publication = models.DateField()
    isbn = models.CharField(max_length=13)
    description = models.TextField()
    statut = models.CharField(max_length=10)
    photo_url = models.CharField(max_length=255)
    
    def __init__(self, titre, auteur, date_publication, isbn, description, statut, photo_url):
        self.titre = titre
        self.auteur = auteur
        self.date_publication = date_publication
        self.isbn = isbn
        self.description = description
        self.statut = statut
        self.photo_url = photo_url