from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'image': forms.HiddenInput,
                   'user': forms.HiddenInput}
