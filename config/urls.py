from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.views import serve
from django.urls import include, path
from django.views.decorators.cache import never_cache
import debug_toolbar


urlpatterns = [
    path('captcha/', include('captcha.urls')),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='main/reset_password.html'),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='main/password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_done.html'),
         name='password_reset_complete'),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    url('', include('social_django.urls', namespace='social')),
    path('', include('DjangoGramm.urls')),
    path('comment/', include('Comments.urls')),
    path('rubric/', include('Rubric.urls')),
    path('followers/', include('FollowingsLikes.urls')),
    path('__debug__/', include(debug_toolbar.urls)),

]


if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
