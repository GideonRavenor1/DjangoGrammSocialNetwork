from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView
from DjangoGramm.services import get_user_likes, get_followers_count
from .services import *


class FollowersListView(LoginRequiredMixin, ListView):
    model = UserGramm
    template_name = 'main/list_followers.html'
    context_object_name = 'followers_users'

    def get_queryset(self):
        return get_followers(self.request.user.pk)[:2]


class FollowersImagesListView(LoginRequiredMixin, ListView):
    model = UserGramm
    template_name = 'main/followers_images.html'

    def get_queryset(self):
        return get_owner(self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = get_following(self.request)
        context['likes'] = get_user_likes(self.request)
        return context


class DynamicFollowingsLoad(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        data = get_data_by_followers(request)
        return JsonResponse({'data': data})


class DynamicFollowings(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        following = get_or_create_follower(request, pk)
        if following[1]:
            following[0].save()
        else:
            following[0].delete()
        data = {
            'user_pk': get_user_page(pk).pk,
            'get_follower': following[1],
            'count_followers': get_followers_count(pk)
        }
        return JsonResponse({'data': data})


class DynamicLikes(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        like = get_or_create_like(request, pk)
        if like[1]:
            like[0].save()
        else:
            like[0].delete()
        data = {
            'like': like[1],
            'count_likes': get_likes_count(pk),
        }
        return JsonResponse({'data': data})

