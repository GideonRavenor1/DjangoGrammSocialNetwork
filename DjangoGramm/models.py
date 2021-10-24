from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from Rubric.models import SubRubric


class UserGramm(AbstractUser):
    GENDER = (
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский')
    )
    middle_name = models.CharField(max_length=50, default='-', blank=True, null=True, verbose_name='Отчество')
    first_login = models.DateTimeField(blank=True, null=True)
    phone = models.CharField(max_length=14, default='-', blank=True, null=True, verbose_name='Номер телефона')
    avatar = models.ImageField(upload_to="media", blank=True, null=True, verbose_name='Аватарка')
    bio = models.TextField(default='-', blank=True, null=True, verbose_name='Биография')
    birthday = models.DateField(default='1900-01-01', blank=True, null=True, verbose_name='День рождения')
    gender = models.CharField(max_length=10, choices=GENDER, default='Мужской', verbose_name='Пол')
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')

    def delete(self, *args, **kwargs):
        for im in self.images.all():
            im.delete()
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('DjangoGramm:by_user', kwargs={'pk': self.pk})


class Image(models.Model):
    image = models.ImageField(upload_to="media", blank=True, null=True, verbose_name='Фотография')
    pub_date = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Дата публикации')
    user = models.ForeignKey(UserGramm, on_delete=models.CASCADE, related_name='images', verbose_name='Пользователь')
    rubric = models.ForeignKey(SubRubric, null=True, on_delete=models.PROTECT, verbose_name='Рубрика')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Показывать на главной странице')

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def __str__(self):
        return 'Фотография пользователя %s' % self.user.username

    def get_absolute_url(self):
        return reverse('Comments:comment_page', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['-pub_date']
