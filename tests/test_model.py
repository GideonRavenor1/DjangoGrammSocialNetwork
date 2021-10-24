from django.test import TestCase
from DjangoGramm import models as d
from Comments import models as c
import tempfile
from Rubric import models as r
from FollowingsLikes import models as f

avatar = tempfile.NamedTemporaryFile(suffix=".jpg").name
image = tempfile.NamedTemporaryFile(suffix=".jpg").name


class TestModels(TestCase):

    def setUp(self):
        self.user = d.UserGramm.objects.create(username='john', password='johnpassword',
                                               email='lennon@thebeatles.com', avatar=avatar,
                                               first_name='Fedor', last_name='Obolikhin',
                                               middle_name='Mikhailovich', phone='89761111111',
                                               bio='bla bla bla')
        self.user2 = d.UserGramm.objects.create(username='kate', password='johnpassword',
                                                email='kate@thebeatles.com', avatar=avatar,
                                                first_name='Katya', last_name='Obolikhina',
                                                middle_name='Mikhailovna', phone='89769999999',
                                                bio='bla bla bla bla bla bla')
        self.super_rubric = r.SuperRubric.objects.create(name='Nature')
        self.rubric = r.Rubric.objects.create(name='Animals', super_rubric=self.super_rubric)
        self.image = d.Image.objects.create(image=image, user=self.user, rubric=self.rubric)
        self.comment = c.Comment.objects.create(image=self.image, user=self.user, content='bla bla')
        self.follow = f.UserFollowing.objects.create(user_id=self.user, following_user_id=self.user2)
        self.follow2 = f.UserFollowing.objects.create(user_id=self.user2, following_user_id=self.user)
        self.like = f.UserLike.objects.create(user=self.user, image=self.image)

    def test_count_models(self):
        self.assertEqual(d.UserGramm.objects.count(), 2)
        self.assertEqual(r.SuperRubric.objects.count(), 1)
        self.assertEqual(r.Rubric.objects.count(), 2)
        self.assertEqual(d.Image.objects.count(), 1)
        self.assertEqual(c.Comment.objects.count(), 1)
        self.assertEqual(f.UserFollowing.objects.count(), 2)
        self.assertEqual(f.UserLike.objects.count(), 1)

    def test_user_models_IsInstance(self):
        self.assertIsInstance(self.user.first_name, str)
        self.assertIsInstance(self.user.last_name, str)
        self.assertIsInstance(self.user.username, str)
        self.assertIsInstance(self.user.password, str)
        self.assertIsInstance(self.user.middle_name, str)
        self.assertIsInstance(self.user.phone, str)
        self.assertIsInstance(self.user.bio, str)
        self.assertIsInstance(self.user.email, str)

    def test_user_model_Equal(self):
        self.assertEqual(self.user.first_name, 'Fedor')
        self.assertEqual(self.user.last_name, 'Obolikhin')
        self.assertEqual(self.user.username, 'john')
        self.assertEqual(self.user.password, 'johnpassword')
        self.assertEqual(self.user.middle_name, 'Mikhailovich')
        self.assertEqual(self.user.phone, '89761111111')
        self.assertEqual(self.user.bio, 'bla bla bla')
        self.assertEqual(self.user.email, 'lennon@thebeatles.com')
        self.assertEqual(self.user.birthday, '1900-01-01')
        self.assertEqual(self.user.gender, 'Мужской')
        self.assertTrue(self.user.avatar is not None)
        self.assertEqual(self.user.avatar, avatar)

    def test_user_model_update(self):
        self.user.first_name = 'Marina'
        self.assertEqual(self.user.first_name, 'Marina')
        self.user.last_name = 'Klimenko'
        self.assertEqual(self.user.last_name, 'Klimenko')
        self.user.username = 'Kate'
        self.assertEqual(self.user.username, 'Kate')
        self.user.password = 'newpassword'
        self.assertEqual(self.user.password, 'newpassword')
        self.user.middle_name = 'Vyacheslavovna'
        self.assertEqual(self.user.middle_name, 'Vyacheslavovna')
        self.user.phone = '897600000011'
        self.assertEqual(self.user.phone, '897600000011')
        self.user.bio = 'new_bio'
        self.assertEqual(self.user.bio, 'new_bio')
        self.user.email = 'marina@yandex.com'
        self.assertEqual(self.user.email, 'marina@yandex.com')
        self.user.birthday = '1994-09-01'
        self.assertEqual(self.user.birthday, '1994-09-01')
        self.user.gender = 'Женский'
        self.assertEqual(self.user.gender, 'Женский')
        avatar2 = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.user.avatar = avatar2
        self.assertEqual(self.user.avatar, avatar2)

    def test_user_model_delete(self):
        self.user2.delete()
        self.assertEqual(d.UserGramm.objects.count(), 1)

    def test_super_rubric_models_IsInstance(self):
        self.assertIsInstance(self.super_rubric.name, str)

    def test_super_rubric_model_Equal(self):
        self.assertEqual(self.super_rubric.name, 'Nature')

    def test_super_rubric_model_update(self):
        self.super_rubric.name = 'Food'
        self.assertEqual(self.super_rubric.name, 'Food')

    def test_rubric_models_IsInstance(self):
        self.assertIsInstance(self.rubric.name, str)

    def test_rubric_model_Equal(self):
        self.assertEqual(self.rubric.name, 'Animals')
        self.assertEqual(self.rubric.super_rubric, self.super_rubric)

    def test_rubric_model_update(self):
        self.rubric.name = 'Cars'
        self.assertEqual(self.rubric.name, 'Cars')
        self.super_rubric2 = r.SuperRubric.objects.create(name='Vehicle')
        self.rubric.super_rubric = self.super_rubric2
        self.assertEqual(self.rubric.super_rubric, self.super_rubric2)

    def test_image_model_Equal(self):
        self.assertTrue(self.image.image is not None)
        self.assertEqual(self.image.image, image)
        self.assertEqual(self.image.user, self.user)
        self.assertEqual(self.image.rubric, self.rubric)

    def test_image_model_update(self):
        self.super_rubric2 = r.SuperRubric.objects.create(name='Vehicle')
        self.rubric2 = r.Rubric.objects.create(name='Cars', super_rubric=self.super_rubric2)
        self.image.rubric = self.rubric2
        self.assertEqual(self.image.rubric, self.rubric2)

    def test_image_model_delete(self):
        self.image.delete()
        self.assertEqual(d.Image.objects.count(), 0)

    def test_comment_models_IsInstance(self):
        self.assertIsInstance(self.comment.content, str)

    def test_comment_model_Equal(self):
        self.assertEqual(self.comment.image, self.image)
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.content, 'bla bla')

    def test_follow_models_Equal(self):
        self.assertEqual(self.follow.user_id, self.user)
        self.assertEqual(self.follow.following_user_id, self.user2)
        self.assertEqual(self.follow2.user_id, self.user2)
        self.assertEqual(self.follow2.following_user_id, self.user)

    def test_follow_models_delete(self):
        self.follow2.delete()
        self.assertEqual(f.UserFollowing.objects.count(), 1)

    def test_like_models_Equal(self):
        self.assertEqual(self.like.user, self.user)
        self.assertEqual(self.like.image, self.image)

    def test_like_models_delete(self):
        self.like.delete()
        self.assertEqual(f.UserLike.objects.count(), 0)
