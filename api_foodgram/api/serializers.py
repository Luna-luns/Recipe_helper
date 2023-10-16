import base64
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.db import transaction
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingCart, Tag)
from rest_framework import serializers
from services import recipes, tags
from users.models import CustomUser, Subscription


class IngredientSerializer(serializers.ModelSerializer):
    """Обработчик ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeReadSerializer(serializers.ModelSerializer):
    """Обработчик получения ингредиентов в рецепте."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientInRecipeCreateSerializer(serializers.ModelSerializer):
    """Обработчик ингредиентов при создании рецепта."""

    id = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class TagSerializer(serializers.ModelSerializer):
    """Обработчик тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class Base64DecodingImageField(serializers.ImageField):
    """Обработчик изображения, декодирующий строку Base64."""

    def to_internal_value(self, data) -> ContentFile:
        """Метод декодирования изображения."""

        if isinstance(data, str) and data.startswith('data:image'):
            image_format, str_image = data.split(';base64,')
            file_extension = image_format.split('/')[-1]
            random_unique_id = uuid.uuid4()
            data = ContentFile(
                content=base64.b64decode(str_image),
                name=random_unique_id.urn[9:] + '.' + file_extension
            )

        return super().to_internal_value(data)


class RecipeInSubscriptionSerializer(serializers.ModelSerializer):
    """Обработчик выдачи рецептов в подписках пользователя."""

    image = Base64DecodingImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class UsernameValidateSerializer:
    """Обработчик проверяет поле username на различие с me."""

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Запрещено использовать зарезервированные имена.')

        return value


class CustomUserSerializer(UsernameValidateSerializer, UserSerializer):
    """Обработчик пользователей для модели CustomUser."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        """Метод проверяет, подписан ли
        текущий пользователь на автора рецепта.
        """

        user = self.context.get('request').user

        if user.is_anonymous:
            return False

        return Subscription.objects.filter(user=user, author=obj).exists()


class CustomUserCreateSerializer(
    UsernameValidateSerializer,
    UserCreateSerializer
):
    """Обработчик для регистрации пользователей."""

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class SubscriptionSerializer(CustomUserSerializer):
    """Обработчик подписок на пользователей."""

    email = serializers.ReadOnlyField(source='author.email')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes_count(self, obj) -> int:
        """Метод, считающий общее количество рецептов пользователя."""

        return obj.recipes.count()

    def get_recipes(self, obj):
        """Метод для получения рецептов."""

        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        all_recipes = recipes.get_user_recipes(obj)

        if recipes_limit:
            all_recipes = all_recipes[:int(recipes_limit)]

        return RecipeInSubscriptionSerializer(all_recipes, many=True).data


class RecipeReadSerializer(serializers.ModelSerializer):
    """Обработчик получения рецептов."""

    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = IngredientInRecipeReadSerializer(
        many=True,
        read_only=True,
        source='ingredientinrecipe_set'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj) -> bool:
        """Метод проверки добавления рецепта в избранное."""

        request = self.context.get('request')

        if request is None or request.user.is_anonymous:
            return False

        return Favorite.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj) -> bool:
        """Метод проверки добавления рецепта в корзину."""

        request = self.context.get('request')

        if request is None or request.user.is_anonymous:
            return False

        return ShoppingCart.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Обработчик создания рецептов."""

    ingredients = IngredientInRecipeCreateSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=tags.get_all_tags(),
        many=True
    )
    image = Base64DecodingImageField(use_url=True)

    class Meta:
        """Мета-параметры сериализатора"""

        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def validate_ingredients(self, value):

        if not value:
            raise serializers.ValidationError({
                'ingredients': 'Необходим хотя бы один ингредиент.'
            })

        ingredients_list = []

        for item in value:
            try:
                ingredient = Ingredient.objects.get(id=item['id'])

                if ingredient in ingredients_list:
                    raise serializers.ValidationError({
                        'ingredients':
                            'Рецепт содержит повторяющиеся ингредиенты.'
                    })

                ingredients_list.append(ingredient)

            except ObjectDoesNotExist:
                raise serializers.ValidationError({
                    'ingredients':
                        'При создании рецепта указан '
                        'несуществующий ингридиент.'
                })

        return value

    def validate_tags(self, value):

        if not value:
            raise serializers.ValidationError({
                'tags': 'Необходим хотя бы один тег.'
            })
        tags_set = set(value)

        if len(value) != len(tags_set):
            raise serializers.ValidationError({
                'tags': 'Рецепт содержит повторяющиеся теги.'
            })

        return value

    def to_representation(self, instance) -> Recipe:
        """Метод представления модели."""

        serializer = RecipeReadSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        )

        return serializer.data

    def create_ingredients(self, ingredients, recipe) -> None:
        """Метод добавления ингредиента."""

        IngredientInRecipe.objects.bulk_create(
            [
                IngredientInRecipe(
                    ingredient_id=elem.get('id'),
                    recipe=recipe,
                    amount=elem.pop('amount')
                )
                for elem in ingredients
            ]
        )

    def create_tags(self, tags, recipe) -> None:
        """Метод добавления тега."""

        recipe.tags.set(tags)

    @transaction.atomic
    def create(self, validated_data) -> Recipe:
        """Метод создания модели Recipe."""

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        user = self.context.get('request').user
        recipe = Recipe.objects.create(**validated_data, author=user)

        self.create_tags(tags, recipe)
        self.create_ingredients(ingredients, recipe)

        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            ingredients_for_recipe = validated_data.pop('ingredients')
            IngredientInRecipe.objects.filter(recipe=instance).delete()
            self.create_ingredients(
                recipe=instance, ingredients=ingredients_for_recipe
            )

        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.set(tags)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class FavoriteSerializer(serializers.ModelSerializer):
    """Обработчик добавления рецепта в список избранного."""

    image = Base64DecodingImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Обработчик добавления рецепта в список покупок."""

    image = Base64DecodingImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
