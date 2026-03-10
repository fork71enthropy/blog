from django.shortcuts import render, get_object_or_404
from .models import Post,Profile
import markdown
# Create your views here.


def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.content_post = markdown.markdown(post.content_post,extensions=['fenced_code','codehilite'])
    return render(request, 'post_detail.html', {'post': post})

def acceuil(request):
    return render(request,'acceuil.html')

def footer(request):
    return render (request, 'footer.html')
