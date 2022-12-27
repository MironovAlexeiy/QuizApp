from django import template

from quizapp.models import UserAnswer

register = template.Library()


@register.simple_tag
def marked_answer(user, opt):
    useranswer = UserAnswer.objects.filter(user=user, answer=opt)
    if useranswer:
        if opt.is_correct:
            return 'correct'
        return 'wrong'
    return ''


@register.simple_tag
def correct_wrong_count(user, taken_quiz):
    correct = user.quiz_answers.filter(answer__is_correct=True, answer__question__quiz=taken_quiz.quiz).count()
    wrong = user.quiz_answers.filter(answer__is_correct=False, answer__question__quiz=taken_quiz.quiz).count()
    return f'{correct} / {wrong}'
