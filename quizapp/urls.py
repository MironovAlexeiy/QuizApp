from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import (CatalogListView, QuizResultView, TakenQuizListVeiw,
                    take_quiz)

app_name = 'quiz'

urlpatterns = [
    path('', CatalogListView.as_view(), name='main'),
    path('taken/', login_required(TakenQuizListVeiw.as_view()), name='taken_quiz_list'),
    path('quiz/<int:quiz_id>/', login_required(take_quiz), name='take_quiz'),
    path('quiz/<int:quiz_id>/userresults/', login_required(QuizResultView.as_view()), name='user_quiz_results'),
]
