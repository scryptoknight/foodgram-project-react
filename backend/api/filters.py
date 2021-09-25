import django_filters as filters

from api.models import Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='fav_filter')
    is_in_shopping_cart = filters.BooleanFilter(method='shop_filter')

    def fav_filter(self, queryset, name, value):
        query = queryset.filter(is_favorited=value)
        return query

    def shop_filter(self, queryset, name, value):
        query = queryset.filter(is_in_shopping_cart=value)
        return query

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
