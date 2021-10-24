from django.contrib import admin
from django.utils.safestring import mark_safe
from Comments.models import Comment


class AdminComment(admin.ModelAdmin):
    list_display = ('image', 'preview', 'user', 'created_at', 'is_active', )
    fields = ('image', 'preview', 'user', 'content', 'created_at', 'is_active', )
    readonly_fields = ('image', 'user', 'preview', 'created_at', 'content')
    list_filter = ('user',)
    search_fields = ('user__username',)

    def preview(self, obj):
        return mark_safe(f'<img src={obj.image.image.url} width="50", height=60">')
    preview.short_description = 'Фотография'


admin.site.register(Comment, AdminComment)
