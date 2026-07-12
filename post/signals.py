from django.db.models.signals import post_delete,post_save #signal qui se déclenche automatiquement après chaque sauvegarde d'un modèle
from django.dispatch import receiver
from django.core.mail import send_mail
from internaute.models import Internaute
from .models import Post,Like_post
from django.urls import reverse
from django.conf import settings


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs): #instance c'est l'objet concret qui vient d'être sauvegardé, le n-uplet
    if created:  # seulement à la création, pas à la modification
        abonnes = Internaute.objects.values_list('email', flat=True)
        post_url = f"{settings.SITE_URL}{reverse('post_detail', args=[instance.pk])}"
        # à ajouter lorsque mon domaine sera à jour !
        for email in abonnes:
            send_mail(
                subject=f'Nouveau post : {instance.title_post}',
                message=f'Un nouveau post vient d\'être publié : {instance.title_post}',
                from_email=None,
                recipient_list=[email],
                fail_silently=True,
            )


@receiver([post_save, post_delete], sender=Like_post)
def sync_post_like_count(sender, instance, **kwargs):
    post = instance.post
    post.nb_like_post = post.likes_recus.count()
    post.save(update_fields=['nb_like_post'])