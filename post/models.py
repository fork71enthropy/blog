from django.db import models
from my_profile.models import Profile
from internaute.models import Internaute


# Create your models here.
# We are waiting for 3 models, Category_Subject, Post_Article, Like_post

class Category(models.Model):
    category_name = models.CharField(unique=True,null=False,max_length=100)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='category')
    class Meta:
        verbose_name_plural = 'Categories'

class Post(models.Model):
    title_post = models.CharField(unique=True,null=False,max_length=100)
    date_post = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='post')
    nb_like_post = models.IntegerField(default=0)
    nb_dislike_post = models.IntegerField(default=0)


#Un internaute peut liker(resp disliker) un post max 1 fois, donc pas besoin d'avoir les deux attributs 
#nb_like_post et nb_dislike_post, il faut les mettre directement dans post.
# Je dois quand même savoir qui a liké quoi, c'est pourquoi je garde Like_post avec les deux ids
class Like_post(models.Model):
    internaute = models.ForeignKey(Internaute,on_delete=models.CASCADE,related_name='likes_donnes')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes_recus')
    # related_name est le nom que j'utilise depuis la classe parente (classe entre parenthèse pour accéder)
    # aux objets enfants (attributs)
    '''
    mon_post.likes_recus.all()  # tous les likes de ce post
    mon_internaute.likes_donnes.all()  # tous les posts likés par cet internaute
    '''

    class Meta:
        unique_together = ('internaute', 'post')

# Je dois revenir sur cette classe Like_post, car je ne sais pas si elle est nécessaire ! 
# Je pense devoir rajouter une ligne pour connecter Post et Internaute, vu qu'un post recois plusieurs likes
# de divers internautes et un internaute peut liker plusieurs posts
# update : mes 3 models le font déjà, tout est correcte, c'est bien modélisé