import django_filters
from django_filters import rest_framework
from recipes.models import Recipe
from rest_framework.filters import SearchFilter
from services import tags


class RecipeFilter(django_filters.FilterSet):
    """ Фильтр списков избранного и покупок."""

    tags = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=tags.get_all_tags(),
        field_name='tags__slug',
        to_field_name='slug'
    )
    is_favorited = rest_framework.BooleanFilter(
        method='get_is_recipe_in_favorited'
    )
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='get_is_recipe_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def get_is_recipe_in_favorited(self, queryset, _, value):
        user = self.request.user

        if value and not user.is_anonymous:
            return queryset.filter(favorites__user=user)

        return queryset

    def get_is_recipe_in_shopping_cart(self, queryset, _, value):
        user = self.request.user

        if value and not user.is_anonymous:
            return queryset.filter(shopping_cart__user=user)

        return queryset


class IngredientFilter(SearchFilter):
    search_param = 'name'
