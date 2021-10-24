from django import forms
from .models import SuperRubric, SubRubric


class SubRubricForm(forms.ModelForm):
    super_rubric = forms.ModelChoiceField(
        queryset=SuperRubric.objects.all(), empty_label=None,
        label='Надрубрика', required=True)

    class Meta:
        model = SubRubric
        fields = '__all__'
