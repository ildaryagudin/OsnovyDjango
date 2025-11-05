from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя"""
    username = None  # Убираем поле username

    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )
    avatar = models.ImageField(
        upload_to='users/avatars/',
        verbose_name='Аватар',
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Номер телефона',
        blank=True,
        null=True
    )
    country = models.CharField(
        max_length=100,
        verbose_name='Страна',
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'  # Поле для авторизации
    REQUIRED_FIELDS = []  # Обязательные поля кроме USERNAME_FIELD

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email