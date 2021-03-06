from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Avg
from django.template.defaultfilters import slugify
from django.utils import timezone


class MovieManager(models.Manager):
    def current(self):
        try:
            return self.get_query_set().filter(when__isnull=False).order_by('-when')[0]
        except IndexError:
            return self.get_query_set().none()


class Movie(models.Model):
    user = models.ForeignKey('auth.User')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    overview = models.TextField()
    tmdb_id = models.CharField(max_length=255)
    poster = models.CharField(max_length=255)
    release_date = models.DateField()
    where = models.CharField(max_length=255, null=True, blank=True)
    when = models.DateTimeField(null=True, blank=True)

    created = models.DateTimeField(default=timezone.now, editable=False)

    objects = MovieManager()

    class Meta:
        ordering = ('-created',)

    def __getattribute__(self, name):
        # TODO: Decide on a better way to do this.
        # Do we really need to generate this? Silly API.
        if name == 'poster':
            return settings.TMDB_IMAGE_URL + 'w500' + object.__getattribute__(self, name)
        return object.__getattribute__(self, name)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movie-detail', kwargs={'slug': self.slug})

    @property
    def thumbnail(self, size):
        return settings.TMDB_IMAGE_URL + 'w{0}'.format(size) + self.poster

    @property
    def score(self):
        avg = Rating.objects.filter(movie=self).aggregate(Avg('score'))['score__avg']
        if avg is not None:
            return round(avg, 1)
        return 0

    @classmethod
    def generate_slug(self, name):
        count = 1
        slug = slugify(name)

        def _get_query(**kwargs):
            if Movie.objects.filter(**kwargs).count():
                return True

        while _get_query(slug=slug):
            slug = slugify(u'{0}-{1}'.format(name, count))
            # make sure the slug is not too long
            while len(slug) > Movie._meta.get_field('slug').max_length:
                name = name[:-1]
                slug = slugify(u'{0}-{1}'.format(name, count))
            count = count + 1
        return slug


class Rating(models.Model):
    movie = models.ForeignKey('Movie')
    user = models.ForeignKey('auth.User')
    score = models.IntegerField()

    class Meta:
        unique_together = ('movie', 'user')

    def __unicode__(self):
        return '{0}: {1} ({2})'.format(self.movie, str(self.score), self.user)

