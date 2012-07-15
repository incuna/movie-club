from django.conf import settings
from django.conf.urls import *
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import AuthComplete, LoginError, MovieDetail, SubmitMovie


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', SubmitMovie.as_view()),
    url(r'^movies/$', SubmitMovie.as_view(), name='movie-create'),
    url(r'^movies/(?P<slug>[\w-]+)/$', MovieDetail.as_view(), name='movie-detail'),
    url(r'^login-error/$', LoginError.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^complete/(?P<backend>[^/]+)/$', AuthComplete.as_view()),
    url(r'', include('social_auth.urls')),
)

urlpatterns += staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
