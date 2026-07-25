# quiz/models.py
from django.db import models
from django.conf import settings
from post.models import Post  # adapte le nom de ton app blog si différent


class Quiz(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="quiz")
    is_published = models.BooleanField(default=False)
    passing_score = models.PositiveIntegerField(default=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quiz de {self.post.title_post}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    base_question_id = models.PositiveIntegerField()
    variant = models.PositiveIntegerField()
    text = models.TextField()
    explanation = models.TextField(blank=True)

    def __str__(self):
        return f"Q{self.base_question_id}.v{self.variant} — {self.text[:50]}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    score = models.PositiveIntegerField()
    passed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tentative {self.id} — {self.quiz} — {'✅' if self.passed else '❌'}"