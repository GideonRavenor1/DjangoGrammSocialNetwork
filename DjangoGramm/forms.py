from django import forms
from .models import UserGramm, Image
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .apps import user_registered
from captcha.fields import CaptchaField


class UserImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('image', 'rubric', 'user', 'is_active')
        widgets = {'user': forms.HiddenInput}


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты.')

    class Meta:
        model = UserGramm
        fields = ('avatar', 'username', 'email', 'first_name', 'last_name',
                  'middle_name', 'gender',  'birthday', 'phone', 'bio')


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                               help_text=password_validation.password_validators_help_text_html())
    repeat_password = forms.CharField(label='Повторите пароль.', widget=forms.PasswordInput,
                                      help_text='Введите пароль повторно для проверки.')
    captcha = CaptchaField(label='Введите текст с картинки', error_messages={'invalid': 'Неправильный текст'})

    def clean_password(self):
        password = self.cleaned_data['password']
        if password:
            password_validation.validate_password(password)
        return password

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        if password and repeat_password and password != repeat_password:
            errors = {'repeat_password': ValidationError('Пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = UserGramm
        fields = ('username', 'email', 'password', 'repeat_password', 'captcha')

