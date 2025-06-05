from django.db import models

class Etudiant(models.Model):
    nom_complet = models.CharField(max_length=255)

class Photo(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/')