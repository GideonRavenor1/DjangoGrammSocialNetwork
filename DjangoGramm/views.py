from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from FollowingsLikes.services import get_follower_true_or_false
from .forms import ChangeUserInfoForm, RegisterUserForm, UserImageForm
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature
from django.contrib.auth import logout
from django.contrib import messages
from .services import *
from .utilities import signer
from django.views import View
from .models import Image


class IndexView(LoginRequiredMixin, ListView):
    model = Image
    template_name = 'main/index.html'
    context_object_name = 'images'
    queryset = get_images()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['likes'] = get_user_likes(self.request)
        return context


class ProfileView(ListView):
    model = Image
    template_name = 'main/profile.html'
    context_object_name = 'images'

    def get_queryset(self):
        return get_images_profile_filter(self.request)


class ProfileImageAddView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Image
    template_name = 'main/profile_image_add.html'
    form_class = UserImageForm
    success_url = reverse_lazy('DjangoGramm:profile')
    success_message = 'Фотография добавленна.'

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['user'] = self.request.user.pk
        return initial


class ProfileImageDeleteView(LoginRequiredMixin, DeleteView):
    model = Image
    template_name = 'main/profile_image_delete.html'
    success_url = reverse_lazy('DjangoGramm:profile')
    success_message = 'Фотография удалена'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class UserPageView(LoginRequiredMixin, DetailView):
    template_name = 'main/by_user.html'
    model = UserGramm
    context_object_name = 'userGramm'

    def get_queryset(self):
        return get_user_followers(self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['get_follower'] = get_follower_true_or_false(self.request, self.object.pk)
        return context


class DjangoLoginView(LoginView):
    template_name = 'main/login.html'


class DjangoLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = UserGramm
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('DjangoGramm:profile')
    success_message = 'Данные пользователя изменены.'

    def setup(self, request, *args, **kwargs):
        self.user_id = get_user_pk(request)
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class DjangoPasswordChangeView(SuccessMessageMixin,
                               LoginRequiredMixin,
                               PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('DjangoGramm:profile')
    success_message = 'Пароль успешно изменен.'


class RegisterUserView(CreateView):
    model = UserGramm
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('DjangoGramm:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = UserGramm
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('DjangoGramm:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = get_user_pk(request)
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS,
                             'Пользователь удален')

        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class DynamicUserImageLoad(LoginRequiredMixin, View):

    @staticmethod
    def get(request, *args, **kwargs):
        data = get_data_by_user_image(request)
        return JsonResponse({'data': data})


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        template = 'main/404_not_found.html'
        return render(request, template)
    return HttpResponse(template.render(request=request))


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    template = check_is_user_activate(username)
    return render(request, template)
