from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, QuizAttempt
from django.urls import reverse


def all_quizzes(request):
    quizzes = Quiz.objects.filter(is_published=True).select_related("post")
    return render(request, "quiz/all_quizzes.html", {"quizzes": quizzes})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == "POST":
        score = 0
        for question in quiz.questions.all():
            selected_id = request.POST.get(f"question_{question.id}")
            if selected_id and question.choices.filter(id=selected_id, is_correct=True).exists():
                score += 1

        passed = score >= quiz.passing_score

        if not request.session.session_key:
            request.session.save()

        QuizAttempt.objects.create(
            quiz=quiz,
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key,
            score=score,
            passed=passed,
        )

        if passed:
            #return redirect("quiz_success", quiz_id=quiz.id)
            return redirect(f"{reverse('quiz_success', args=[quiz.id])}?score={score}")
        return render(request, "quiz/quiz_failed.html", {"quiz": quiz, "score": score})

    return render(request, "quiz/quiz_detail.html", {"quiz": quiz})




def quiz_success(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    score = request.GET.get("score")
    total = quiz.questions.count()
    return render(request, "quiz/quiz_success.html", {"quiz": quiz, "score": score, "total": total})

"""def quiz_success(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, "quiz/quiz_success.html", {"quiz": quiz})
"""