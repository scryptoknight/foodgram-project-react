from django.contrib import admin

from users.models import Follow, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'id')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('author', 'user', 'id')
    search_fields = ('following__username', 'follower__username')


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
