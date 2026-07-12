from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Liker_com

@receiver([post_save, post_delete], sender=Liker_com)
def sync_comment_like_count(sender, instance, **kwargs):
    comment = instance.comment
    comment.nb_like_com = comment.like_com.count()
    comment.save(update_fields=['nb_like_com'])