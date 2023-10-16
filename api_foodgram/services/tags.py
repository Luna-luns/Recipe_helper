from recipes.models import Tag


def get_all_tags() -> Tag:
    """Возвращает список всех тегов."""

    return Tag.objects.all()
