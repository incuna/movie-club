from datetime import datetime
import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.base import View
import requests
from social_auth.backends.exceptions import AuthFailed
from social_auth.views import complete

from .forms import RatingForm
from .models import Movie, Rating


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


class MovieDetail(CreateView):
    form_class = RatingForm
    model = Rating
    success_url = '.'
    template_name = 'movie_club/movie_detail.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.movie = self.get_movie()
        self.object.save()
        return super(MovieDetail, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(MovieDetail, self).get_context_data(**kwargs)
        context['movie'] = self.get_movie()
        return context

    def get_movie(self):
        return Movie.objects.get(slug=self.kwargs.get('slug'))


class MovieList(ListView):
    model = Movie


class SubmitMovie(TemplateView):
    template_name = 'home.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(SubmitMovie, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.POST['movie-data'])

        args = (settings.TMDB_API_URL, data['id'], settings.TMDB_API_KEY)
        url = '{0}movie/{1}?api_key={2}'.format(*args)
        r = requests.get(url)
        all_data = json.loads(r.content)

        Movie.objects.create(
            user=request.user,
            name=data['title'],
            slug=Movie.generate_slug(data['title']),
            overview=all_data['overview'],
            tmdb_id=data['id'],
            poster=data['poster_path'],
            release_date=datetime.strptime(all_data['release_date'], '%Y-%m-%d')
        )
        return HttpResponseRedirect(reverse('movie-list'))

