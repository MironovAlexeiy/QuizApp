from django import forms
from django.forms.utils import ValidationError

from .models import Answer, Question, UserAnswer


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('title', 'image')


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(BaseAnswerInlineFormSet, self).clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Выберите правильный вариант(ы) ответа', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None,
        label='Вариатны ответов')

    class Meta:
        model = UserAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super(TakeQuizForm, self).__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answer_set.order_by('?')
