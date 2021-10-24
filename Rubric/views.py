from django.contrib.auth.mixins import LoginRequiredMixin
from DjangoGramm.services import get_current_rubric, get_images_rubric_filter, get_user_likes
from django.views.generic import ListView
from Rubric.models import Rubric


class ByRubricView(LoginRequiredMixin, ListView):
    template_name = 'main/by_rubric_detail.html'
    context_object_name = 'current_rubric'
    model = Rubric

    def get_queryset(self):
        return get_current_rubric(self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = get_images_rubric_filter(context['current_rubric'].pk)
        context['likes'] = get_user_likes(self.request)
        return context



