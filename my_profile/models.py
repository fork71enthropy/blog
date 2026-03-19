from django.db import models

# Create your models here.
# We are waiting for 5 models, Profile,Author,Project,Book,Ecrire 

# Every programmer is self-taught !

# Django ajoute un champ id à chaque model qui hérite de models.Model
class Profile(models.Model):
    bio_description = models.TextField(null=False)
    github_link = models.URLField(max_length=50, unique=True, null=True, blank=True)
    linkedin_link = models.URLField(max_length=50, unique=True, null=True, blank=True)
    def __str__(self):
        return f"Profile {self.id}"
    
class Author(models.Model):
    author_name = models.CharField(null=False, max_length=100)
    bio_link = models.URLField(max_length=100, unique=True)
    def __str__(self):
        return f"Author {self.author_name}"
    
class Project(models.Model):
    project_name = models.CharField(null=False, max_length=100)
    github_link = models.URLField(max_length=50, unique=True, null=False, blank=False)
    #Dans Project j'ajoute une clé étrangère parce que un Profile a 0 à n projects tandis qu'un project
    #est rataché à un et un seul profile
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='projects')

class Book(models.Model):
    title_book = models.CharField(null=False, max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    filename_path = models.CharField(max_length=100,unique=True)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='books')
    authors = models.ManyToManyField(Author, related_name='books')

    


'''
Pas besoin de le faire, une ligne avec ManyToManyField suffit largement !
class Ecrire(models.Model):
    book = models.CompositePrimaryKey(Book,on_delete=models.CASCADE)
    author = models.CompositePrimaryKey(Author,on_delete=models.CASCADE)

Le ManyToManyField est bidirectionnel, je le déclare d'un seul côté et Django gère automatiquement la
 relation dans les deux sens.
'''



