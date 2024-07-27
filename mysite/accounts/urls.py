from django.urls import path
from .views import register
from .views import UserRegisterView, UserLoginView, PasswordResetCustomView, verify_email

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify/<int:pk>/', verify_email, name='verify_email'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('password_reset/', PasswordResetCustomView.as_view(), name='password_reset'),
    path('register/', register, name='register'),
]
