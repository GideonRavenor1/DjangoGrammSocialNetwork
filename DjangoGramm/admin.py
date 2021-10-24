from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import UserGramm, Image
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
import datetime
from .utilities import send_activation_notification


def send_activation_notifications(model_admin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    model_admin.message_user(request, 'Письма с требованиями отправлены')


send_activation_notifications.short_description = 'Отправка писем с требованем активации'


class NonActivatedFilter(admin.SimpleListFilter):
    title = 'Прошли активацию?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Прошли'),
            ('threedays', 'Не прошли более 3 дней'),
            ('week', 'Не прошли более недели'),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False, date_joined=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False, date_joined=d)


class UserGrammAdmin(UserAdmin):
    list_display = ('__str__', 'is_activated', 'is_staff', 'date_joined', 'username', 'email', 'first_name', 'last_name',)
    list_filter = (NonActivatedFilter,)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_activated', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'get_avatar')}),
        (_('Дополнительная информация'),
         {'fields': ('phone', 'avatar', 'middle_name', 'gender', 'birthday', 'bio')}),
    )
    readonly_fields = ('last_login', 'date_joined', 'get_avatar')
    actions = (send_activation_notifications,)

    def get_avatar(self, obj):
        return mark_safe(f'<img src={obj.avatar.url} width="50", height=60">')

    get_avatar.short_description = "Аватарка"


class AdminImage(admin.ModelAdmin):
    list_display = ('user', 'image', 'pub_date', 'preview', 'rubric', 'is_active')
    fields = ('user', 'image', 'pub_date', 'preview', 'rubric', 'is_active')
    readonly_fields = ('preview', 'pub_date')
    list_filter = ('user', 'pub_date', 'rubric')
    search_fields = ('user__username', 'rubric__name', 'rubric__super_rubric__name')

    def preview(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50", height=60">')
    preview.short_description = 'Фотография'


admin.site.register(UserGramm, UserGrammAdmin)
admin.site.register(Image, AdminImage)
admin.site.site_header = 'Администрирование сайта DjangoGramm'
admin.site.index_title = 'Администрирование сайта DjangoGramm'
