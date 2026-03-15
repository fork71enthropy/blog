from django.shortcuts import render,get_object_or_404
from .models import Profile
from post.views import render_markdown

# Create your views here.
def my_profile_presentation(request):
    profile = get_object_or_404(Profile,pk=1)
    profile.content_rendered = render_markdown(profile.bio_description)
    return render(request,'my_profile/personal.html',{'profile':profile})


































