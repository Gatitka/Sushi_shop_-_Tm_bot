from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    '''Модель категорий блюд.'''
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        unique=True
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name',)

    def clean(self) -> None:
        self.name = self.name.strip().lower()
        return super().clean()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ Модель для описания ингредиентов."""
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=24,
        db_index=True,
        verbose_name='Ед-ца измерения'
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'
        ordering = ('id', )

    def __str__(self):
        return self.name

    def clean(self) -> None:
        self.name = self.name.lower()
        self.measurement_unit = self.measurement_unit.lower()
        if Ingredient.objects.filter(name=self.name).exists():
            raise ValidationError('Ингредиент с таким названием уже есть')
        super().clean()


class Dish(models.Model):
    '''Модель блюд.'''
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Название',
        help_text='Добавьте название готового блюда.'
    )
    price = models.IntegerField(    # цена
        validators=[MinValueValidator(1)]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='recipes',
        help_text='Добавьте категорию блюда.'
    )
    # image = models.ImageField(
    #     upload_to='recipe/images/',
    #     help_text='Добавьте изображение готового блюда.'
    # )
    # text = models.TextField(
    #     help_text='Введите способ приготовления.'
    # )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='DishIngredient',
        verbose_name='Ингредиенты',
        related_name='ingredient',
        help_text='Добавьте ингредиенты рецепта.'
    )
    add_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True
    )

    class Meta:
        ordering = ['-add_date']
        verbose_name = 'блюдо'
        verbose_name_plural = 'блюдо'

    def __str__(self):
        return self.name

    def load_ingredients(self, ingredients):
        lst_ingrd = [
            DishIngredient(
                ingredient=ingredient["id"],
                amount=ingredient["amount"],
                recipe=self,
            )
            for ingredient in ingredients
        ]
        DishIngredient.objects.bulk_create(lst_ingrd)


class DishIngredient(models.Model):
    """ Модель для сопоставления связи блюда и ингридиентов."""
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        verbose_name='Блюдо',
        related_name='ingredient',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        verbose_name='Ингредиент',
        related_name='Dish'
    )
    # amount = models.PositiveSmallIntegerField(
    #     verbose_name='Кол-во',
    #     validators=[MinValueValidator(1)]
    # )

    class Meta:
        ordering = ['dish']
        verbose_name = 'блюдо-ингредиенты'
        verbose_name_plural = 'блюдо-ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['dish', 'ingredient'],
                name='unique_dish_ingredient'
            )
        ]
