from django.contrib import admin

from users.models import Favorit

from .models import Category, Dish, DishIngredient, Ingredient

admin.site.register(Category)


class DishIngredientAdmin(admin.TabularInline):
    model = DishIngredient
    min_num = 1


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    """Настройки админ панели блюд."""
    list_display = ('pk', 'name', 'price', 'in_favorits', 'category')  # + category
    list_filter = ('name', ) # + category
    search_fields = ('name',)  # + category
    inlines = (DishIngredientAdmin,)

    def in_favorits(self, obj):
        return Favorit.objects.filter(dish=obj).count()
    in_favorits.short_description = 'В избранном'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Настройки отображения данных таблицы Ingredient."""
    list_display = ('pk', 'name', 'measurement_unit')
    list_filter = ('name',)
