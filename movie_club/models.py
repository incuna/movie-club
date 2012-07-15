from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify


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

    def __unicode__(self):
        return self.score

