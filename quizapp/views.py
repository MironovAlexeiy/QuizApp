from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from django.views.generic.list import ListView

from common.views import TitleMixin

from .forms import TakeQuizForm
from .models import Question, Quiz, TakenQuiz


class CatalogListView(TitleMixin, ListView):
    model = Quiz
    title = 'Главная страница'
    template_name = 'quiz/catalog.html'

    def get_queryset(self):
        qs = super(CatalogListView, self).get_queryset()
        user = self.request.user
        if user.is_authenticated:
            take_quizzes = user.taken_quiz.values_list('quiz_id', flat=True)
            return qs.exclude(pk__in=take_quizzes).filter(is_public=True)\
                .annotate(question_count=Count('question')).filter(question_count__gte=1)
        return qs.filter(is_public=True).annotate(question_count=Count('question'))\
            .filter(question_count__gte=1)


class TakenQuizListVeiw(TitleMixin, ListView):
    model = TakenQuiz
    title = 'Пройденные тесты'
    template_name = 'quiz/taken_quiz.html'

    def get_queryset(self):
        qs = super(TakenQuizListVeiw, self).get_queryset()
        return qs.filter(user=self.request.user).select_related('quiz', 'quiz__category')


class QuizResultView(TitleMixin, View):
    title = 'Результаты тестов'
    template_name = 'quiz/quiz_result.html'

    def get(self, request, *args, **kwargs):
        quiz = Quiz.objects.filter(id=kwargs.get('quiz_id')).first()
        taken_quiz = TakenQuiz.objects.filter(user=request.user)
        questions = Question.objects.filter(quiz=quiz)
        context = {
            'title': self.title,
            'questions': questions,
            'quiz': quiz,
            'percent': taken_quiz[0].percent}
        return render(request, self.template_name, context)


def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user = request.user

    if user.quizzes.filter(id=quiz_id).exists():
        return render(request, 'quiz/take_quiz_form.html')

    total_questions = quiz.question_set.count()
    unanswered_questions = user.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                user_answer = form.save(commit=False)
                user_answer.user = user
                user_answer.save()
                if user.get_unanswered_questions(quiz).exists():
                    return redirect('quiz:take_quiz', quiz_id)
                else:
                    correct_answer = user.quiz_answers.filter(answer__question__quiz=quiz,
                                                              answer__is_correct=True).count()
                    percent = round((correct_answer/total_questions) * 100, 2)
                    TakenQuiz.objects.create(user=user, quiz=quiz, score=correct_answer, percent=percent)
                    user.score = TakenQuiz.objects.filter(user=user).aggregate(Sum('score'))['score__sum']
                    user.save()
                    if percent < 50:
                        messages.warning(request, f'Ваш результат составляет {percent}%')
                    else:
                        messages.success(request, f'Поздравляю! Вы прошли тест {quiz.title} с результатом в {percent}%')
                    return redirect('quiz:user_quiz_results', quiz_id)
    else:
        form = TakeQuizForm(question=question)

    context = {
        'title': f'{quiz.title}',
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress,
        'answered_questions': total_questions - total_unanswered_questions,
        'total_questions': total_questions}

    return render(request, 'quiz/take_quiz_form.html', context)
