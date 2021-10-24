from django.db import models
from DjangoGramm.models import UserGramm, Image


class UserFollowing(models.Model):
    user_id = models.ForeignKey(UserGramm, related_name="following",
                                on_delete=models.CASCADE, verbose_name='Подписчик')
    following_user_id = models.ForeignKey(UserGramm, related_name="followers",
                                          on_delete=models.CASCADE, verbose_name='Подписан')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')

    def __str__(self):
        return '%s - %s' % (self.user_id.username, self.following_user_id.username)

    class Meta:
        verbose_name = 'Подписки пользователя'
        verbose_name_plural = 'Подписки пользователей'
        ordering = ['-user_id']


class UserLike(models.Model):
    user = models.ForeignKey(UserGramm, related_name="likes",
                             on_delete=models.CASCADE, verbose_name='Пользователь')
    image = models.ForeignKey(Image, related_name="likes",
                              on_delete=models.CASCADE, verbose_name='Фотография')
    like = models.BooleanField(default=True, db_index=True, verbose_name='Поставил лайк')

    def __str__(self):
        return 'Пользователь %s поставил лайк' % self.user.username

    class Meta:
        verbose_name = 'Лайки пользователя'
        verbose_name_plural = 'Лайки пользователей'
