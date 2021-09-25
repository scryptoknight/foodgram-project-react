from rest_framework import serializers

from api.models import Recipe
from users.models import Follow, User


class RecipeTinySerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    queryset = User.objects.all()
    user = serializers.PrimaryKeyRelatedField(queryset=queryset)
    author = serializers.PrimaryKeyRelatedField(queryset=queryset)

    class Meta:
        model = Follow
        fields = ('user', 'author')

    def validate(self, data):
        user = self.context.get('request').user
        author_id = data['author'].id
        if user.pk == author_id:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        follow_exist = Follow.objects.filter(
            user=user,
            author__id=author_id
        ).exists()
        if follow_exist:
            raise serializers.ValidationError(
                'Вы подписаны')

        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return FollowReadSerializer(
            instance.author,
            context=context).data


class FollowReadSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.BooleanField(read_only=True)
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_recipes(self, obj):
        num = self.context["request"].query_params.get('recipes_limit')
        if num:
            num = int(num)
            recipes = obj.recipes.all()[:num]
        else:
            recipes = obj.recipes.all()
        return RecipeTinySerializer(recipes, many=True).data


class ListFavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, author):
        request = self.context.get('request')
        if request.user and request.user.is_authenticated:
            return Follow.objects.filter(
                user=request.user, author=author
            ).exists()
        return False
