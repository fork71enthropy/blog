from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from post.models import Post
from .models import Comment, Liker_com
from .forms import CommentForm

@login_required
def add_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.internaute = request.user
            comment.save()
    return redirect('post_detail', pk=post.pk)


@login_required
def toggle_comment_like(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    like, created = Liker_com.objects.get_or_create(internaute=request.user, comment=comment)
    if not created:
        like.delete()
    return redirect('post_detail', pk=comment.post.pk)