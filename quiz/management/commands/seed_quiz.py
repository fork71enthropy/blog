import importlib
from django.core.management.base import BaseCommand, CommandError
from post.models import Post
from quiz.models import Quiz, Question, Choice


class Command(BaseCommand):
    help = "Seed a quiz from a data module in quiz/quiz_data/"

    def add_arguments(self, parser):
        parser.add_argument("module_name", type=str, help="e.g. csrf_quiz")

    def handle(self, *args, **options):
        module_name = options["module_name"]
        try:
            data_module = importlib.import_module(f"quiz.quiz_data.{module_name}")
        except ModuleNotFoundError:
            raise CommandError(f"Module quiz.quiz_data.{module_name} introuvable")

        data = data_module.QUIZ_DATA
        post = Post.objects.get(id=data["post_id"])

        quiz, created = Quiz.objects.get_or_create(
            post=post,
            defaults={"passing_score": data["passing_score"], "is_published": False},
        )
        if not created:
            self.stdout.write(self.style.WARNING(f"Quiz déjà existant pour '{post}', questions ajoutées en plus"))

        for q_data in data["questions"]:
            question = Question.objects.create(
                quiz=quiz,
                base_question_id=q_data["base_question_id"],
                variant=1,
                text=q_data["text"],
                explanation=q_data["explanation"],
            )
            for choice_text, is_correct in q_data["choices"]:
                Choice.objects.create(question=question, text=choice_text, is_correct=is_correct)

        self.stdout.write(self.style.SUCCESS(
            f"{len(data['questions'])} questions créées pour le quiz '{quiz}'"
        ))