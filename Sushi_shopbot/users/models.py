from django.contrib.auth.models import AbstractUser
# from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models

from catalog.models import Dish


# class UserRoles(models.TextChoices):
#     ADMIN = ('admin', 'Администратор')
#     USER = ('user', 'Пользователь')


class User(AbstractUser):
    first_name = models.CharField(
        'Имя',
        max_length=150,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150
    )
    phone = models.CharField(
        'Телефон',
        max_length=100,
        validators=[MinLengthValidator(8)]
    )
    Tm_ID = models.CharField(
        'Telegram_ID',
        max_length=100,
        validators=[MinLengthValidator(4)]
    )
    password = models.CharField(
        'Пароль',
        max_length=100,
        validators=[MinLengthValidator(8)]
    )
    email = models.EmailField(
        'Email',
        max_length=254,
        unique=True
    )
    # role = models.CharField(
    #     'Роль',
    #     max_length=9,
    #     choices=UserRoles.choices,
    #     default=UserRoles.USER
    # )

    class Meta:
        ordering = ['id']
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    # def is_admin(self):
    #     return self.role == UserRoles.ADMIN or self.is_superuser


class Favorit(models.Model):
    """ Модель для добавления блюд в избранное пользователя."""
    favoriter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorits',
        verbose_name='В избранном у'
    )

    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name='favorited',
        verbose_name='Блюда'
    )

    class Meta:
        ordering = ['favoriter']
        verbose_name = 'избранное'
        verbose_name_plural = 'избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['favoriter', 'dish'],
                name='unique_favoriter_dish'
            )
        ]

    def __str__(self):
        return f'{self.favoriter} -> {self.dish}'
