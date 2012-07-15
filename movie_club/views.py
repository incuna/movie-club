import json

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView
from django.views.generic.base import View
from social_auth.backends.exceptions import AuthFailed
from social_auth.views import complete

from .models import Movie


class AuthComplete(View):
    def get(self, request, *args, **kwargs):
        backend = kwargs.pop('backend')
        try:
            return complete(request, backend, *args, **kwargs)
        except AuthFailed:
            messages.error(request, "Your Google Apps domain isn't authorized for this app")
            return HttpResponseRedirect(reverse('login'))


class LoginError(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(status=401)


class MovieDetail(DetailView):
    model = Movie


class MovieList(ListView):
    model = Movie


class SubmitMovie(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(SubmitMovie, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()

        try:
            movie = Movie.objects.create(
                name=request.POST['title'],
                slug=Movie.generate_slug(request.POST['title']),
                tmdb_id=request.POST['id'],
                thumbnail=request.POST['poster_path']
            )
        except Exception as e:
            data = {'error': True, 'content': e}
        else:
            data = {'error': False, 'content': movie.get_absolute_url()}

        return HttpResponse(json.dumps(data), content_type='application/json')

