from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    can_create = models.BooleanField(default=False)
    score = models.PositiveSmallIntegerField(default=0)

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers.filter(answer__question__quiz=quiz) \
            .values_list('answer__question_id', flat=True)
        questions = quiz.question_set.exclude(pk__in=answered_questions)
        return questions
