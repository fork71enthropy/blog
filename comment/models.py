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
    nb_like_com = models.IntegerField(default=0)
    nb_dislike_com = models.IntegerField(default=0)
    def __str__(self):
        return f"Comment {self.id}"
    
class Liker_com(models.Model):
    internaute = models.ForeignKey(Internaute,on_delete=models.CASCADE,related_name='like_com')
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='like_com')

    class Meta:
        unique_together = ('internaute', 'comment')
    































