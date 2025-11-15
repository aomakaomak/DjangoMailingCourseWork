from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import RegisterView, activate_account


app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='mailing:index'), name='logout'),

    path('activate/<uidb64>/<token>/', activate_account, name='activate'),

]