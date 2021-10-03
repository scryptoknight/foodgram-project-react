from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.models import (FavorRecipe, Ingredient, Recipe, RecipeComponent,
                        ShoppingList, Tag)
from users.serializers import UserSerializer


MIN_COOKING_TIME = 1
MAX_COOKING_TIME = 32766


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='id',
        queryset=Ingredient.objects.all()
    )
    name = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='name',
        read_only=True
    )
    measurement_unit = serializers.SlugRelatedField(
        source='ingredient.measurement_unit',
        slug_field='name',
        read_only=True
    )

    class Meta:
        model = RecipeComponent
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()
    measurement_unit = serializers.SlugRelatedField(
        source='ingredient.measurement_unit',
        slug_field='name',
        read_only=True
    )

    class Meta:
        model = Ingredient
        fields = ('id', 'amount', 'measurement_unit')

    def validate(self, attrs):
        if not Ingredient.objects.filter(pk=attrs['id']).exists:
            raise serializers.ValidationError(
                {
                    'ingredients': f'ингредиент с id {attrs["id"]} не найден'
                },
            )
        ingredients = self.initial_data.get('ingredients')
        for ingredient in ingredients:
            if int(ingredient.get('amount')) <= 0:
                raise serializers.ValidationError(
                    ('Убедитесь, что значение количества '
                     'ингредиента больше 0')
                )
        attrs['ingredients'] = ingredients
        return attrs


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeComponentSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='id',
        queryset=Ingredient.objects.all()
    )
    name = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='name',
        read_only=True
    )
    measurement_unit = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='measurement_unit',
        read_only=True
    )

    class Meta:
        model = RecipeComponent
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeWriteSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        slug_field='id'
    )
    cooking_time = serializers.IntegerField()
    ingredients = IngredientWriteSerializer(many=True)
    author = UserSerializer(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'tags', 'ingredients', 'name',
                  'image', 'text', 'cooking_time')

    def validate(self, attrs):
        cooking_time = self.initial_data.get('cooking_time')
        if (cooking_time is None or
                int(cooking_time) < MIN_COOKING_TIME or int(cooking_time) > MAX_COOKING_TIME):
            raise serializers.ValidationError(
                f'Время приготовления не может быть меньше {MIN_COOKING_TIME} '
                f'и больше {MAX_COOKING_TIME}'
            )
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                {'ingredients':
                    'Список ингредиентов не получен'}
            )
        ingredients = attrs['ingredients']
        for ingredient in ingredients:
            if ingredient['amount'] <= 0:
                raise serializers.ValidationError(
                    'Увеличьте количество ингридиентов;'
                )
        return attrs

    def create_update_method(self, validated_data, recipe=None):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        if recipe:
            recipe.component_recipes.all().delete()
        else:
            recipe = Recipe.objects.create(**validated_data)
        ingredient_instances = []
        seen_ingredients = set()
        for ingredient in ingredients:
            id = ingredient['id']
            if id in seen_ingredients:
                raise serializers.ValidationError(
                    f'Найден дублирующийся ингредиент id {id}'
                )
            seen_ingredients.add(id)
            ingr_id = Ingredient.objects.get(pk=id)
            amt = ingredient['amount']
            ingredient_instances.append(
                RecipeComponent(ingredient=ingr_id, recipe=recipe, amount=amt)
            )
        for ingredient in ingredients:
            if int(ingredient['amount']) <= 1:
                raise serializers.ValidationError(('Убедитесь, что значение количества '
                                                   'ингредиента больше или равно 1.')
                                                  )
        RecipeComponent.objects.bulk_create(ingredient_instances)
        recipe.tags.set(tags)
        return recipe

    def create(self, validated_data):
        return self.create_update_method(validated_data)

    def update(self, instance, validated_data):
        instance = self.create_update_method(validated_data, recipe=instance)
        instance.name = validated_data.pop('name')
        instance.text = validated_data.pop('text')
        if validated_data.get('image') is not None:
            instance.image = validated_data.pop('image')
        instance.cooking_time = validated_data.pop('cooking_time')
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField('get_ingredients')
    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_ingredients(self, recipe):
        queryset = RecipeComponent.objects.filter(recipe=recipe)
        return RecipeComponentSerializer(queryset, many=True).data


class ShoppingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingList
        fields = '__all__'

    def validate(self, attrs):
        if not Ingredient.objects.filter(pk=attrs['recipes'].id).exists:
            raise serializers.ValidationError(
                {
                    'ingredients':
                        f'Ингредениет с id {attrs["recipes"]} не найден'
                },
            )
        author = self.context.get('request').user
        recipe = attrs['recipes']
        recipe_exists = ShoppingList.objects.filter(
            author=author,
            recipes=recipe
        ).exists()
        if recipe_exists:
            raise serializers.ValidationError(
                'Рецепт уже в корзине'
            )
        return attrs


class FavorSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if not Recipe.objects.filter(pk=attrs['recipes'].id).exists:
            raise serializers.ValidationError(
                {
                    'recipes': f'Рецепт с id {attrs["recipes"]} не найден'
                }
            )
        follow_exists = FavorRecipe.objects.filter(
            author=attrs['author'],
            recipes=attrs['recipes']
        ).exists()
        if follow_exists:
            raise serializers.ValidationError(
                'Вы уже добавили рецепт в избранное'
            )
        return attrs

    class Meta:
        model = FavorRecipe
        fields = '__all__'
