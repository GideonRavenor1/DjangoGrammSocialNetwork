from .models import UserGramm
from Rubric.models import SubRubric


def wall_context_processor(request):
    context = {'rubrics': SubRubric.objects.all().select_related("super_rubric"),
               'users': UserGramm.objects.exclude(pk=request.user.pk).values("pk", "username")}
    return context
