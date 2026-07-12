from django.shortcuts import render, get_object_or_404
from .models import Post,Like_post
import markdown
from django.contrib.auth.decorators import login_required
from comment.forms import CommentForm

# Create your views here.


def render_markdown(content):
    return markdown.markdown(
        content,
        extensions=['fenced_code', 'codehilite','tables']
    )


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.content_rendered = render_markdown(post.content_post)

    user_has_liked = (
        request.user.is_authenticated
        and post.likes_recus.filter(internaute=request.user).exists()
    )

    liked_comment_ids = set()
    if request.user.is_authenticated:
        liked_comment_ids = set(
            request.user.like_com.values_list('comment_id', flat=True)
        )

    return render(request, 'post/post_detail.html', {
        'post': post,
        'user_has_liked': user_has_liked,
        'liked_comment_ids': liked_comment_ids,
        'comment_form': CommentForm(),
    })


def allposts(request):
    posts = Post.objects.all()
    for post in posts:
        post.content_rendered = render_markdown(post.content_post)
    return render(request, 'post/accueil.html', {'posts': posts})



@login_required
def toggle_post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like_post.objects.get_or_create(internaute=request.user, post=post)
    if not created:
        like.delete()
    return redirect('post_detail', pk=post.pk)











