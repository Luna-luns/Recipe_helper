from recipes.models import Recipe
from users.models import CustomUser


def get_all_recipes() -> Recipe:
    """Возвращает список всех рецептов."""

    return Recipe.objects.all()


def get_user_recipes(obj: CustomUser) -> Recipe:
    """Возвращает все рецепты пользователя."""

    return obj.recipes.all()
