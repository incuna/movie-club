from django.conf import settings
from django.conf.urls import *
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.http import HttpResponse

from .views import AuthComplete


def login_error(request, *args, **kwargs):
    return HttpResponse('LOGIN ERROR!')

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^complete/(?P<backend>[^/]+)/$', AuthComplete.as_view()),
    url(r'', include('social_auth.urls')),
)

urlpatterns += staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
