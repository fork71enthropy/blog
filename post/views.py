from django.shortcuts import render, get_object_or_404
from .models import Post
import markdown
# Create your views here.


def render_markdown(content):
    return markdown.markdown(
        content,
        extensions=['fenced_code', 'codehilite']
    )

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.content_rendered = render_markdown(post.content_post)
    return render(request, 'post/post_detail.html', {'post': post})


def allposts(request):
    posts = Post.objects.all()
    for post in posts:
        post.content_rendered = render_markdown(post.content_post)
    return render(request, 'post/accueil.html', {'posts': posts})
















