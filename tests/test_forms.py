from unittest import TestCase
from DjangoGramm import forms as d, models as m
from Comments import forms as c
from Rubric import models as r
import tempfile
from django.core import mail

avatar = tempfile.NamedTemporaryFile(suffix=".jpg").name
image = tempfile.NamedTemporaryFile(suffix=".jpg").name


class TestForms(TestCase):

    def test_change_user_info_form(self):
        form_data = {
            'username': 'john',
            'email': 'lennon@thebeatles.com',
            'first_name': 'Ann',
            'last_name': 'Karenina',
            'bio': 'Notorious by dying due to train',
            'phone': '893424423',
            'birthday': '1900-01-01',
            'gender': 'Мужской',
            'middle_name': 'asddasd',
            'avatar': avatar

        }
        form = d.ChangeUserInfoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form(self):
        self.user = m.UserGramm.objects.create_user(username='freddi', password='johnpassword',
                                                    email='lennon@thebeatles.com', avatar=avatar,
                                                    first_name='Fedor', last_name='Obolikhin',
                                                    middle_name='Mikhailovich', phone='89761111111',
                                                    bio='bla bla bla')
        self.super_rubric = r.SuperRubric.objects.create(name='Nature')
        self.rubric = r.Rubric.objects.create(name='Animals', super_rubric=self.super_rubric)
        self.image = m.Image.objects.create(image=image, user=self.user, rubric=self.rubric)
        form_data = {
            'user': self.user,
            'image': self.image,
            'content': 'bla bla bla'
        }
        form = c.CommentForm(data=form_data)
        self.assertTrue(form.is_valid())


class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail('Subject here', 'Here is the message.',
                       'obolihin.fedor@gmail.com', ['to@example.com'],
                       fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject here')
