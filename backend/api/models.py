from django.db import models
from django.db.models.base import Model
from django.urls import reverse
from django.contrib.auth import get_user_model

from colorfield.fields import ColorField

User = get_user_model()


class Unit(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Название'
        )

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'


class Ingredient(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Название'
        )
    units = models.ForeignKey(
        Unit,
        related_name='Recipe',
        verbose_name='Тэги',
        on_delete=models.PROTECT
        )

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Название')
    hex = ColorField(
        format='hexa',
        default='#FF0000',
        verbose_name='hex-цвет')
    slug = models.SlugField(
        max_length=150,
        verbose_name='URL Тэга',
        unique=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        blank=False,
        null=False,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Author'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название рецепта',
        blank=False,
        )
    image = models.ImageField(
        verbose_name='Картинка',
        blank=False,
        )
    description = models.TextField(
        verbose_name='Описание рецепта',
        blank=False,
        )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='Recipe',
        verbose_name='Тэги',
        blank=False,
        )
    tags = models.ManyToManyField(
        Tag,
        related_name='Recipe',
        verbose_name='Тэги',
        blank=False,
        )
    time = models.IntegerField(
        verbose_name='Время приготовления',
        blank=False,
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        blank=False,
        )

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        blank=False,
        null=False,
        verbose_name='Recipe'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        blank=False,
        null=False,
        verbose_name='Ingredient'
    )
    amount = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name='Ingredient amount'
    )

    class Meta:
        verbose_name = 'Ингридиент рецепта'
        verbose_name_plural = 'Ингридиенты рецепта'


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_favorites',
        blank=False,
        null=False,
        verbose_name='User'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        blank=False,
        null=False,
        verbose_name='Recipe'
    )

    class Meta:
        verbose_name = 'Избраное'
        verbose_name_plural = 'Избраное'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        blank=False,
        null=False,
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        blank=False,
        null=False,
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author'
            )
        ]