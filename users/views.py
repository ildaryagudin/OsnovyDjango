from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.mail import send_mail
from .forms import UserRegisterForm, UserLoginForm
from .models import User


class RegisterView(CreateView):
    """CBV для регистрации пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        """Обработка успешной регистрации с отправкой письма"""
        response = super().form_valid(form)

        # Автоматически логиним пользователя после регистрации
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=password)

        if user is not None:
            login(self.request, user)

        # Отправка приветственного письма
        try:
            send_mail(
                subject='Добро пожаловать в наш магазин!',
                message=f'''Здравствуйте, {user.email}!

Добро пожаловать в наш интернет-магазин! Мы рады, что вы присоединились к нам.

Ваш аккаунт был успешно создан. Теперь вы можете:
- Просматривать каталог товаров
- Добавлять новые продукты
- Редактировать свои товары
- Публиковать статьи в блоге

Если у вас возникнут вопросы, не стесняйтесь обращаться в нашу службу поддержки.

С уважением,
Команда магазина''',
                from_email=None,  # Используется DEFAULT_FROM_EMAIL
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            # Если отправка письма не удалась, продолжаем работу
            print(f"Ошибка отправки письма: {e}")

        messages.success(
            self.request,
            f'Вы успешно зарегистрировались! Добро пожаловать, {user.email}!'
        )
        return response


class UserLoginView(LoginView):
    """CBV для авторизации пользователя"""
    template_name = 'users/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        """Обработка успешной авторизации"""
        response = super().form_valid(form)
        messages.success(self.request, f'Добро пожаловать, {self.request.user.email}!')
        return response


class LogoutView(View):
    """CBV для выхода пользователя"""

    def get(self, request):
        logout(request)
        messages.info(request, 'Вы успешно вышли из системы.')
        return redirect('catalog:home')