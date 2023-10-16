from django.contrib.admin import ModelAdmin, register

from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('user', 'recipe')


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@register(IngredientInRecipe)
class IngredientInRecipeAdmin(ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'author', 'get_favorites')
    list_filter = ('author', 'name', 'tags')

    def get_favorites(self, obj):
        """Метод для подсчёта общего числа
        добавлений рецепта в избранное.
        """

        return obj.favorites.count()


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    list_display = ('user', 'recipe')


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'color', 'slug')
