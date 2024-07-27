from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import UserLoginForm
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from .models import CustomUser
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.contrib.auth.forms import UserCreationForm


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm


class UserRegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def verify_email(request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # Send email verification
        send_mail(
            'Подтверждение регистрации',
            'Пожалуйста, подтвердите свою регистрацию, перейдя по следующей ссылке: {0}'.format('http://127.0.0.1:8000/accounts/verify/{0}'.format(user.id)),
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


class PasswordResetCustomView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            new_password = get_random_string(8)
            user.password = make_password(new_password)
            user.save()
            send_mail(
                'Новый пароль',
                f'Ваш новый пароль: {new_password}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        return super().form_valid(form)

    def register(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('home')  # Замените 'home' на путь к вашему домашнему или начальной странице
        else:
            form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})