from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    users = models.ManyToManyField('auth.User', through='Rating')

    def __unicode__(self):
        return self.name


class Rating(models.Model):
    movie = models.ForeignKey('Movie')
    user = models.ForeignKey('auth.User')
    score = models.IntegerField()

    def __unicode__(self):
        return self.score

