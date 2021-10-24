from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from DjangoGramm.models import Image
from DjangoGramm.services import get_image, get_comment, get_user_likes
from .forms import CommentForm


class CommentPageAddView(LoginRequiredMixin, DetailView, FormMixin):
    template_name = 'main/comment_page.html'
    model = Image
    form_class = CommentForm

    def get_initial(self):
        user = self.request.user.pk
        return {'image': self.object, 'user': user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = get_comment(self.object.pk)
        context['likes'] = get_user_likes(self.request)
        context['img'] = get_image(self.object.pk)
        return context

    def post(self, request, *args, **kwargs):
        c_form = self.form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS, 'Комментарий добавлен')
        else:
            messages.add_message(request, messages.WARNING, 'Комментарий не добавлен')
        return redirect('Comments:comment_page', pk=kwargs['pk'])
