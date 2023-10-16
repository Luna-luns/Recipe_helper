import re

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True
    )
    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=re.compile(r'^[\w.@+-]+\Z'),
                message='Проверьте правильность написания никнейма'
            )
        ]
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        max_length=150
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150
    )

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        CustomUser,
        verbose_name='Подписчик',
        related_name='subscriber',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор рецепта',
        related_name='author',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]

    def __str__(self):
        return f'{self.user} подписался на {self.author}'
