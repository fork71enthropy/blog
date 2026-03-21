from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# We are waiting for 1 model, Internaute

# Problème réglé en 3 lignes
class Internaute(AbstractUser):
    abonne = models.BooleanField(null=False,default=False)







'''
class Internaute(models.Model):

    # nb : ne jamais stocker un password en clair dans un charfield, la bonne pratique est d'utiliser le 
    # model abstractUser intégré qui gère automatiquement le système d'authentification. C'est chiant ces 
    # histoires de gestion automatique !
    abonne = models.BooleanField(null=False)


pour l'authentification, ne pas oublier d'ajouter dans settings.py
AUTH_USER_MODEL = 'internaute.Internaute'


internaute/models.py — vérifier que tu as bien abonne = BooleanField(default=False)
internaute/forms.py — créer un ModelForm avec les champs email, mot de passe, nom, prénom
internaute/views.py — une vue qui traite le formulaire et crée l'objet
internaute/urls.py — brancher l'URL /inscription/
'''