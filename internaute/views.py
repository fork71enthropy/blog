from django.shortcuts import render,redirect
from .models import Internaute
from .forms import InscriptionForm
from django.core.mail import send_mail,BadHeaderError
from django.contrib import messages
import smtplib

# Create your views here.

def inscription(request):
    my_mail = "noreply@opus-symmetry.fr"
    form = InscriptionForm() # affiche un formulaire vide lorsque arrive sur la page
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if(form.is_valid()):
            internaute = form.save() # => mail de bienvenue
            try:
                send_mail(
                    subject="Bienvenue sur devlog.py",
                    message=f"Premier mail envoyé à l'utilisateur {internaute.first_name} {internaute.last_name}.",
                    from_email=f"{my_mail}",
                    recipient_list=[internaute.email],
                    fail_silently=False,
                )
                messages.success(request, "Tu es maintenant abonné à devlog.py !")

            except BadHeaderError :
                # Quelqu'un a injecté des headers malveillants dans le sujet ou le message
                messages.error(request, "Erreur lors de l'envoi du mail.")
            except smtplib.SMTPException:
                # Le serveur mail est down, credentials incorrects, etc.
                messages.error(request,"Erreur lors de l'envoi du mail")
            return redirect('/')
    return render(request,'internaute/inscription.html',{'form':form})


#pip freeze > requirements.txt pour update mon fichier 

def ajout_commentaire(request):
    # à remplir, sans oublier les unit tests


