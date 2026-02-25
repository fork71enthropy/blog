from django.db import models

# Create your models here.
from django.db import models


class Internaute(models.Model):
    pseudo = models.CharField(max_length=50, unique=True)
    adresse_mail = models.EmailField(unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    mot_de_passe = models.CharField(max_length=255)
    abonne = models.BooleanField(default=False)

    def __str__(self):
        return self.pseudo


class Profile(models.Model):
    internaute = models.OneToOneField(
        Internaute, on_delete=models.CASCADE, related_name='profile'
    )
    bio = models.TextField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Profile de {self.internaute.pseudo}"


class Project(models.Model):
    internaute = models.ForeignKey(
        Internaute, on_delete=models.CASCADE, related_name='projects'
    )
    name = models.CharField(max_length=200)
    github_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    internaute = models.ForeignKey(
        Internaute, on_delete=models.CASCADE, related_name='books'
    )
    title_book = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    filename = models.CharField(max_length=255, blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title_book


class Subject(models.Model):
    subject_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.subject_name


class Post(models.Model):
    internaute = models.ForeignKey(
        Internaute, on_delete=models.CASCADE, related_name='posts'
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.SET_NULL, null=True, related_name='posts'
    )
    post_title = models.CharField(max_length=200)
    date_post = models.DateTimeField(auto_now_add=True)
    nb_like_post = models.PositiveIntegerField(default=0)
    nb_dislike_post = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.post_title


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    internaute = models.ForeignKey(
        Internaute, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    nb_like_comment = models.PositiveIntegerField(default=0)
    nb_dislike_comment = models.PositiveIntegerField(default=0)
    harmfull = models.BooleanField(default=False)

    def __str__(self):
        return f"Commentaire de {self.internaute.pseudo} sur {self.post.post_title}"


# Table d'association pour les likes de posts
class PostLike(models.Model):
    internaute = models.ForeignKey(
        Internaute, on_delete=models.CASCADE, related_name='post_likes'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes'
    )

    class Meta:
        unique_together = ('internaute', 'post')

    def __str__(self):
        return f"{self.internaute.pseudo} like {self.post.post_title}"


# Table d'association pour les likes de commentaires
class CommentLike(models.Model):
    internaute = models.ForeignKey(
        Internaute, on_delete=models.CASCADE, related_name='comment_likes'
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='likes'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comment_likes'
    )

    class Meta:
        unique_together = ('internaute', 'comment')

    def __str__(self):
        return f"{self.internaute.pseudo} like commentaire {self.comment.id}"
