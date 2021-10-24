from django.shortcuts import get_object_or_404
from django.urls import Resolver404
from Comments.models import Comment
from Rubric.models import Rubric
from .models import Image, UserGramm
from FollowingsLikes.models import UserLike
from django.db.models import Count


def get_user_followers(arg):
    return UserGramm.objects.filter(pk=arg).prefetch_related("following", "followers").\
            defer("is_staff", "is_activated", "date_joined", "is_active", "last_login",
                  "password", "is_superuser", "first_login")\
            .annotate(count_followers=Count("followers__id"))


def get_user_likes(request):
    return UserLike.objects.filter(user=request.user.pk).values_list("image", flat=True)


def get_images():
    return Image.objects.filter(is_active=True).select_related("user", "rubric").prefetch_related("rubric__super_rubric", "likes")\
        .only("image", "pk", "rubric__id", "rubric__name", "rubric__super_rubric", "user__avatar", "user__id", "user__username")\
        .annotate(count=Count("likes"))


def get_images_rubric_filter(args):
    return Image.objects.filter(rubric=args, is_active=True).select_related("user", "rubric").prefetch_related("rubric__super_rubric", "likes")\
        .only("image", "pk", "rubric__id", "rubric__name", "rubric__super_rubric", "user__avatar", "user__id", "user__username")\
        .annotate(count=Count("likes"))


def get_images_profile_filter(args):
    return Image.objects.filter(user=args.user.pk).select_related("rubric").select_related("rubric__super_rubric")


def get_current_rubric(args):
    rubric = Rubric.objects.filter(pk=args).only("pk")
    if rubric:
        return rubric[0]
    raise Resolver404


def get_user_page(args):
    user = get_object_or_404(UserGramm, pk=args)
    return user


def get_followers_count(args):
    user = get_object_or_404(UserGramm, pk=args)
    followers = user.followers.count()
    return followers


def get_image(args):
    image = get_object_or_404(Image, pk=args)
    return image


def get_comment(args):
    return Comment.objects.filter(image=args, is_active=True)


def check_is_user_activate(username):
    user = get_object_or_404(UserGramm, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return template


def get_user_pk(args):
    return args.user.pk


def get_data_by_user_image(request):
    last_user_image_id = request.GET.get('lastUserImageId')
    more_images = get_more_user_images(last_user_image_id, request)
    if not more_images:
        return False
    data = []
    for image in more_images:
        obj = {
            'pk': image.pk,
            'image': image.image.url,
            'rubric': image.rubric.name,
            'super_rubric': image.rubric.super_rubric.name

        }
        data.append(obj)

    data[-1]['last_user_image'] = True
    return data


def get_more_user_images(args, request):
    return Image.objects.filter(pk__lt=int(args), user=request.user.pk)[:2]

