from django.db import models
from DjangoGramm.models import Image, UserGramm


class Comment(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, verbose_name='Фотография')
    user = models.ForeignKey(UserGramm, on_delete=models.PROTECT, verbose_name='Пользователь')
    content = models.TextField(verbose_name='Содержание')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Показывать на экране')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликован')

    def __str__(self):
        return 'Комментарий пользователя %s' % self.user.username

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
