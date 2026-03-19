from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# We are waiting for 1 model, Internaute

# Problème réglé en 3 lignes
class Internaute(AbstractUser):
    abonne = models.BooleanField(null=False,default=False)







'''
class Internaute(models.Model):
    pseudo = models.TextField(null=False,unique=True)
    adresse_mail = models.EmailField(null=False,max_length=100,unique=True)
    date_creation = models.DateTimeField(null=False,auto_now_add=True)
    # nb : ne jamais stocker un password en clair dans un charfield, la bonne pratique est d'utiliser le 
    # model abstractUser intégré qui gère automatiquement le système d'authentification. C'est chiant ces 
    # histoires de gestion automatique !
    password = models.CharField(null=False,max_length=100)
    abonne = models.BooleanField(null=False)


pour l'authentification, ne pas oublier d'ajouter dans settings.py
AUTH_USER_MODEL = 'internaute.Internaute'
'''