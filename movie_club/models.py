from django.db import models
from django.core.urlresolvers import reverse


class Movie(models.Model):
    users = models.ManyToManyField('auth.User', through='Rating')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    tmdb_id = models.CharField(max_length=255)
    thumbnail = models.CharField(max_length=255)
    where = models.CharField(max_length=255, null=True, blank=True)
    when = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movie-detail', kwargs={'slug': self.slug})

    @classmethod
    def generate_slug(name):
        return name.lower()


class Rating(models.Model):
    movie = models.ForeignKey('Movie')
    user = models.ForeignKey('auth.User')
    score = models.IntegerField()

    def __unicode__(self):
        return self.score

