from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.shortcuts import get_object_or_404
from DjangoGramm.models import Image, UserGramm
from DjangoGramm.services import get_user_page, get_image
from FollowingsLikes.models import UserFollowing, UserLike


def get_or_create_follower(request, pk):
    return UserFollowing.objects.get_or_create(user_id=request.user,
                                               following_user_id=get_user_page(pk))


def get_follower_true_or_false(request, pk):
    return UserFollowing.objects.filter(user_id=request.user,
                                        following_user_id=pk).only("pk").exists()


def get_followers(obj):
    return UserFollowing.objects.filter(following_user_id=obj).select_related("user_id") \
        .only("user_id_id", "user_id__avatar", "user_id__username")


def get_following(request):
    image_list = Image.objects.exclude(pk=request.user.pk).select_related("user", "rubric") \
        .prefetch_related("user__followers", "rubric__super_rubric", "likes") \
        .filter(user__followers__user_id=request.user.pk) \
        .only("image", "pk", "rubric__id", "rubric__name", "rubric__super_rubric", "user__avatar", "user__id",
              "user__username") \
        .annotate(count=Count("likes"))
    return image_list


def get_or_create_like(request, pk):
    return UserLike.objects.get_or_create(user=request.user,
                                          image=get_image(pk))


def get_like_or_false(request, pk):
    try:
        like = UserLike.objects.get(user=request.user,
                                    image=get_image(pk))
    except ObjectDoesNotExist:
        like = False
    return like


def get_likes_count(args):
    image = get_object_or_404(Image, pk=args)
    likes = image.likes.count()
    return likes


def get_data_by_followers(request):
    last_followers_id = request.GET.get('lastUserId')
    more_followers = get_more_followers(last_followers_id, request.user.pk)
    if not more_followers:
        return False
    data = []
    for follower in more_followers:
        try:
            avatar = follower.user_id.avatar.url
        except ValueError:
            avatar = '/static/image/def_ava.jpg'
        obj = {
            'pk': follower.user_id.pk,
            'user': follower.user_id.username,
            'avatar': avatar,
        }
        data.append(obj)

    data[-1]['last_follower'] = True
    return data


def get_more_followers(args, request):
    result = UserFollowing.objects.filter(following_user_id=request, user_id__lt=args)
    return result[:2]


def get_owner(args):
    return UserGramm.objects.filter(pk=args).only("pk")
