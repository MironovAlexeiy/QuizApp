from django.db import models

from users.models import User


class Category(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории тестов'
        ordering = ('title', )


class Quiz(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='author_quiz')
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=False)
    users = models.ManyToManyField(to=User, related_name='quizzes')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        ordering = ('title', )
        unique_together = ('slug', 'category')


class Question(models.Model):
    quiz = models.ForeignKey(to=Quiz, on_delete=models.CASCADE)
    title = models.TextField()
    image = models.ImageField(upload_to='quiz/%Y/%m/%d', blank=True)

    def __str__(self):
        return f'{self.title[:30]} к тесту {self.quiz}'

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class TakenQuiz(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='taken_quiz')
    quiz = models.ForeignKey(to=Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.PositiveSmallIntegerField(default=0)
    percent = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.quiz.title


class UserAnswer(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(to=Answer, on_delete=models.CASCADE, related_name='user_answer')

    def __str__(self):
        return f'{self.answer.title}  | { self.answer.question.title} |  {self.user}'
