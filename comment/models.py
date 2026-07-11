from django.db import models
from post.models import Post
from internaute.models import Internaute
# Create your models here.
# TODO : We are waiting for 2 models, Comment and Liker_com

class Comment(models.Model):
    text = models.TextField(null=False)
    comment_date = models.DateTimeField(auto_now_add=True)
    harmfull = models.BooleanField(null=False,default=False) 
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comment')
    internaute = models.ForeignKey(Internaute,on_delete=models.CASCADE,related_name='comment')
    def __str__(self):
        return f"Comment {self.id}"
    
class Liker_com(models.Model):
    internaute = models.ForeignKey(Internaute,on_delete=models.CASCADE,related_name='like_com')
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='like_com')
    nb_like_com = models.IntegerField(default=0)
    nb_dislike_com = models.IntegerField(default=0)
    












class Profile(models.Model):
    bio_description = models.TextField(null=False)
    github_link = models.URLField(max_length=50, unique=True, null=True, blank=True)
    linkedin_link = models.URLField(max_length=50, unique=True, null=True, blank=True)
    def __str__(self):
        return f"Profile {self.id}"


class Book(models.Model):
    title_book = models.CharField(null=False, max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    filename_path = models.CharField(max_length=100,unique=True)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='books')
    authors = models.ManyToManyField(Author, related_name='books')
    def __str__(self):
        return f"{self.title_book}"






















