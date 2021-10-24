from django.test import TestCase
from django.urls import reverse
from django.test.client import Client
from DjangoGramm import models as d
from Rubric import models as r
import tempfile

image = tempfile.NamedTemporaryFile(suffix=".jpg").name


class NotAuthorizedPageTests(TestCase):

    def setUp(self):
        self.user = d.UserGramm.objects.create_user(username='fred', password='fredpassword',
                                                    email='fred@thebeatles.com')
        self.super_rubric = r.SuperRubric.objects.create(name='Other')
        self.rubric = r.Rubric.objects.create(name='Games', super_rubric=self.super_rubric)
        self.image = d.Image.objects.create(image=image, user=self.user)

    def test_index_page_status_code_not_authorized(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 302)

    def test_index_view_url_by_name_not_authorized(self):
        response = self.client.get(reverse('DjangoGramm:index'))
        self.assertEquals(response.status_code, 302)

    def test_rubric_page_status_code_not_authorized(self):
        response = self.client.get('/rubric/by/1/')
        self.assertEquals(response.status_code, 302)

    def test_rubric_view_url_by_name_not_authorized(self):
        response = self.client.get(reverse('Rubric:by_rubric',
                                           args=[1]))
        self.assertEquals(response.status_code, 302)

    def test_about_page_status_code_not_authorized(self):
        response = self.client.get('/about/')
        self.assertEquals(response.status_code, 200)

    def test_about_view_url_by_name_not_authorized(self):
        response = self.client.get(reverse('DjangoGramm:other',
                                           args=['about']))
        self.assertEquals(response.status_code, 200)

    def test_register_page_status_code_not_authorized(self):
        response = self.client.get('/accounts/register/')
        response2 = self.client.post('/accounts/register/',
                                     {'username': 'john',
                                      'email': 'lennon@thebeatles.com',
                                      'password': 'ytrewq199325',
                                      'repeat_password': 'ytrewq199325',
                                      'captcha': 'PASSED'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response2.status_code, 200)

    def test_register_view_url_by_name_not_authorized(self):
        response = self.client.get(reverse('DjangoGramm:register'))
        response2 = self.client.post(reverse('DjangoGramm:register'),
                                     {'username': 'john',
                                      'email': 'lennon@thebeatles.com',
                                      'password': 'ytrewq199325',
                                      'repeat_password': 'ytrewq199325',
                                      'captcha': 'PASSED'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response2.status_code, 200)

    def test_reset_password_status_code_not_authorized(self):
        response = self.client.get('/reset_password/')
        response2 = self.client.post('/reset_password/',
                                     {'email': 'lennon@thebeatles.com'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response2.status_code, 302)

    def test_reset_password_view_url_by_name_not_authorized(self):
        response = self.client.get(reverse('reset_password'))
        response2 = self.client.post(reverse('reset_password'),
                                     {'email': 'lennon@thebeatles.com'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response2.status_code, 302)

    def test_by_user_status_code_not_authorized(self):
        response = self.client.get(f'/by_user/{self.user.pk}/')
        response2 = self.client.post(f'/by_user/{self.user.pk}/')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response2.status_code, 302)

    def test_by_user_view_url_by_name_not_authorized(self):
        response = self.client.get(reverse('DjangoGramm:by_user',
                                   args=[self.user.pk]))
        response2 = self.client.post(reverse('DjangoGramm:by_user',
                                     args=[self.user.pk]))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response2.status_code, 302)

    def test_comment_status_code_not_authorized(self):
        response = self.client.get(f'/comment/image/{self.image.pk}/')
        response2 = self.client.post(f'/comment/image/{self.image.pk}/', {'context': 'bla bla bla'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response2.status_code, 302)

    def test_comment_view_url_by_name_not_authorized(self):
        response = self.client.get(reverse('Comments:comment_page',
                                           args=[self.image.pk]))
        response2 = self.client.post(reverse('Comments:comment_page',
                                             args=[self.image.pk]), {'context': 'bla bla bla bla'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response2.status_code, 302)

    def test_like_status_code_not_authorized(self):
        response = self.client.get(f'/comment/image/{self.image.pk}/')
        response2 = self.client.post(f'/comment/image/{self.image.pk}/')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response2.status_code, 302)

    def test_like_view_url_by_name_not_authorized(self):
        response = self.client.get(reverse('Comments:comment_page',
                                           args=[self.image.pk]))
        response2 = self.client.post(reverse('Comments:comment_page',
                                             args=[self.image.pk]))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response2.status_code, 302)


class AuthorizedPageTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = d.UserGramm.objects.create_user(username='john', password='johnpassword',
                                                    email='lennon@thebeatles.com')
        self.super_rubric = r.SuperRubric.objects.create(name='Nature')
        self.rubric = r.Rubric.objects.create(name='Animals', super_rubric=self.super_rubric)
        self.image = d.Image.objects.create(image=image, user=self.user)
        self.client.login(username='john', password='johnpassword')

    def test_login(self):
        self.assertTrue(self.user.is_authenticated)

    def test_index_page_status_code_authorized(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_index_view_url_by_name_authorized(self):
        response = self.client.get(reverse('DjangoGramm:index'))
        self.assertEqual(response.status_code, 200)

    def test_rubric_page_status_code_authorized(self):
        response = self.client.get(f'/rubric/by/{self.rubric.pk}/')
        self.assertEquals(response.status_code, 200)

    def test_rubric_view_url_by_name_authorized(self):
        response = self.client.get(reverse('Rubric:by_rubric',
                                           args=[self.rubric.pk]))
        self.assertEquals(response.status_code, 200)

    def test_profile_my_image_page_status_code(self):
        response = self.client.get('/accounts/profile/')
        self.assertEquals(response.status_code, 200)

    def test_profile_my_image_view_url_by_name(self):
        response = self.client.get(reverse('DjangoGramm:profile'))
        self.assertEquals(response.status_code, 200)

    def test_profile_delete_image_page_status_code(self):
        response = self.client.get(f'/accounts/profile/delete/{self.image.pk}/')
        response2 = self.client.post(f'/accounts/profile/delete/{self.image.pk}/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response2.status_code, 302)

    def test_profile_delete_image_view_url_by_name(self):
        response = self.client.get(reverse('DjangoGramm:profile_image_delete', args=[self.image.pk]))
        response2 = self.client.post(reverse('DjangoGramm:profile_image_delete', args=[self.image.pk]))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response2.status_code, 302)

    def test_profile_add_image_page_status_code(self):
        response = self.client.get('/accounts/profile/add/')
        self.assertEquals(response.status_code, 200)

    def test_profile_add_image_view_url_by_name(self):
        response = self.client.get(reverse('DjangoGramm:profile_image_add'))
        self.assertEquals(response.status_code, 200)

    def test_profile_change_info_page_status_code(self):
        response = self.client.get('/accounts/profile/change/')
        response2 = self.client.post('/accounts/profile/change/', {'first_name': 'Pasha'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response2.status_code, 200)

    def test_profile_change_info_view_url_by_name(self):
        response = self.client.get(reverse('DjangoGramm:profile_change'))
        response2 = self.client.post(reverse('DjangoGramm:profile_change'), {'first_name': 'Pasha'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response2.status_code, 200)

    def test_profile_change_password_page_status_code(self):
        response = self.client.get('/accounts/password/change/')
        self.assertEquals(response.status_code, 200)

    def test_profile_change_password_view_url_by_name(self):
        response = self.client.get(reverse('DjangoGramm:password_change'))
        self.assertEquals(response.status_code, 200)

    def test_profile_delete_page_status_code(self):
        response = self.client.get('/accounts/profile/delete/')
        response2 = self.client.post('/accounts/profile/delete/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response2.status_code, 302)

    def test_profile_delete_view_url_by_name(self):
        response = self.client.get(reverse('DjangoGramm:profile_delete'))
        response2 = self.client.post(reverse('DjangoGramm:profile_delete'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response2.status_code, 302)

    def test_by_user_page_status_code(self):
        response = self.client.get(f'/by_user/{self.user.pk}/')
        self.assertEquals(response.status_code, 200)

    def test_by_user_view_url_by_name(self):
        response = self.client.get(reverse('DjangoGramm:by_user',
                                           args=[self.user.pk]))
        self.assertEquals(response.status_code, 200)

    def test_comment_page_status_code(self):
        response = self.client.get(f'/comment/image/{self.image.pk}/')
        response2 = self.client.post(f'/comment/image/{self.image.pk}/', {'context': 'bla bla bla'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response2.status_code, 302)

    def test_comment_view_url_by_name(self):
        response = self.client.get(reverse('Comments:comment_page',
                                           args=[self.image.pk]))
        response2 = self.client.post(reverse('Comments:comment_page',
                                             args=[self.image.pk]), {'context': 'bla bla bla'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response2.status_code, 302)

    def test_like_ajax(self):
        response = self.client.post(f'/followers/ajax/count-likes/{self.image.pk}/')
        self.assertEquals(response.status_code, 200)

    def test_following_ajax(self):
        response = self.client.post(f'/followers/ajax/followings/{self.user.pk}/')
        self.assertEquals(response.status_code, 200)

    def test_logout(self):
        self.client.logout()
        response = self.client.get('/')
        self.assertEquals(response.status_code, 302)
