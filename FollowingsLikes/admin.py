from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import UserFollowing, UserLike


class AdminFollowers(admin.ModelAdmin):
    list_display = ('user_id', 'following_user_id', 'created')
    fields = ('user_id', 'following_user_id', 'created')
    readonly_fields = ('created',)
    list_filter = ('user_id', 'following_user_id',)
    search_fields = ('user_id__username', 'following_user_id__username',)


class AdminLikes(admin.ModelAdmin):
    list_display = ('user', 'image', 'preview', 'like', )
    fields = ('user', 'image', 'preview', 'like')
    readonly_fields = ('like', 'preview')
    list_filter = ('user',)
    search_fields = ('user__username',)

    def preview(self, obj):
        return mark_safe(f'<img src={obj.image.image.url} width="50", height=60">')
    preview.short_description = 'Фотография'


admin.site.register(UserFollowing, AdminFollowers)
admin.site.register(UserLike, AdminLikes)
