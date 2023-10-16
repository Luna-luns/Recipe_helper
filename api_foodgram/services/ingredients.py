from recipes.models import Ingredient


def get_all_ingredients() -> Ingredient:
    """Возвращает список всех ингредиентов."""

    return Ingredient.objects.all()
