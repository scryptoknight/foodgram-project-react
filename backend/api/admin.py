from django.contrib import admin

from .models import Unit, Ingredient, Tag, Recipe, Favourite, Follow


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author',
                    'description', 'time', 'created_at', 'count_in_favourites')
    list_display_links = ('id', 'title',)
    search_fields = ('title', 'description',)
    empty_value_display = '-пусто-'
    firelds = ('title', 'author', 'description', 'time',
               'created_at', 'tags', 'ingredients')
    list_filter = ('title', 'author', 'tags',)

    def count_in_favourites(self, obj):
        return obj.favorited_by.all().count()


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'hex', 'slug')
    empty_value_display = '-пусто-'
    list_filter = ('title',)
    search_fields = ('title',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'units',)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    empty_value_display = '-пусто-'


class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = '-пусто-'


admin.site.register(Unit)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favourite, FavouriteAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
