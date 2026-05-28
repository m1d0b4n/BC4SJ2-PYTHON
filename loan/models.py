from django.db import models
from django.contrib.auth.models import User

class Livre(models.Model):
    TITRE = models.CharField(max_length=200)
    STATUT_CHOICES = [
        ('disponible', 'Disponible'),
        ('emprunté', 'Emprunté'),
    ]
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='disponible',
    )

    def __str__(self):
        return self.TITRE


class Emprunt(models.Model):
    id_utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    id_livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_retour_prevue = models.DateTimeField()
    date_retour_effectif = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.id_utilisateur.username} - {self.id_livre.TITRE}"