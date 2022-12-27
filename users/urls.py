from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import UserLoginView, UserRegistrationView

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('<int:user_id>/', login_required(UserDetailView.as_view()), name='user_detail'),
]
