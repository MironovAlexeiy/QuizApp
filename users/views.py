from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from common.views import TitleMixin

from .forms import UserLoginForm, UserRegistrationForm


class UserLoginView(TitleMixin, LoginView):
    title = 'Вход'
    form_class = UserLoginForm
    template_name = 'users/login.html'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    title = 'Регистрация'
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_message = 'Для продолжения выполните вход'
    success_url = reverse_lazy('users:login')


# class StudentDetail(View):
#     """Show Details of a Student"""
#
#     def get(self, request, **kwargs):
#         student = User.objects.get(id=kwargs['user_id'])
#         subjects = student.taken_quiz.all() \
#             .values('quiz__category__title') \
#             .annotate(score=Sum('score')) \
#             .order_by('-score')
#
#         return render(request, 'users/user_detail.html',
#                       {'student': student, 'subjects': subjects})


# class UserDetailView(TitleMixin, DetailView):
#     title = 'Личный кабинет'
#     model = User
#     template_name = 'users/user_detail.html'
#     pk_url_kwarg = 'user_id'
#
#     def get_context_data(self, **kwargs):
#         context = super(UserDetailView, self).get_context_data(**kwargs)
#         # context['subject'] = self.queryset.taken_quiz.all().values('quiz__category__title') \
#         #     .annotate(score=Sum('score'))
#         return context
