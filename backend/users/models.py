from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import BooleanField, Count, Value


class UserQuerySet(models.QuerySet):
    def follow_recipes(self, user=None):
        queryset = self.filter(
            following__user=user
        ).order_by('pk').prefetch_related('recipes').annotate(
            is_subscribed=Value(True, output_field=BooleanField()),
            recipes_count=Count('recipes__author')
        )
        return queryset


class CustomUserManager(UserManager.from_queryset(UserQuerySet)):
    use_in_migration = False


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email', unique=True, null=True
    )
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    objects = UserManager()
    ext_objects = CustomUserManager()

    def __str__(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'.strip()
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('pk', )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    def __str__(self):
        return f'Подписка {self.user.username} на {self.author.username}'

    class Meta:
        ordering = ('pk', )
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
