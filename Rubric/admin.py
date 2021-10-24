from django.contrib import admin
from Rubric.forms import SubRubricForm
from Rubric.models import SubRubric, SuperRubric


class SubRubricInline(admin.TabularInline):
    model = SubRubric


class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)


class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm


admin.site.register(SuperRubric, SuperRubricAdmin)
admin.site.register(SubRubric, SubRubricAdmin)
