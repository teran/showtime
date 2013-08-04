import datetime

from django.db import models


class Inode(models.Model):
    path = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return str(self.pk)

class Hardlink(models.Model):
    inode = models.ForeignKey(Inode, related_name='hardlinks')
    token = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return self.token

class Cover(models.Model):
    digest = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return self.digest

class Genre(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return self.name

class TVShow(models.Model):
    title = models.CharField(max_length=255)
    cover = models.ForeignKey(Cover, related_name='tvshows', blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    genre = models.ForeignKey(Genre, related_name='tvshows', blank=True, null=True)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return self.title

class Season(models.Model):
    season = models.IntegerField()
    tvshow = models.ForeignKey(TVShow, related_name='seasons')
    cover = models.ForeignKey(Cover, related_name='seasons', blank=True, null=True)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return str(self.season)

    def sorted_episodes(self):
        return self.episodes.order_by('episode')

class Episode(models.Model):
    title = models.CharField(max_length=255)
    cover = models.ForeignKey(Cover, related_name='episodes', blank=True, null=True)
    episode = models.IntegerField(blank=True, null=True)
    tvshow = models.ForeignKey(TVShow, related_name='episodes')
    season = models.ForeignKey(Season, related_name='episodes', blank=True, null=True)
    inode = models.ForeignKey(Inode, related_name='episodes')
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return self.title


class Movie(models.Model):
    title = models.CharField(max_length=255)
    cover = models.ForeignKey(Cover, related_name='movies')
    year = models.IntegerField(blank=True, null=True)
    genre = models.ForeignKey(Genre, related_name='movies')
    inode = models.ForeignKey(Inode, related_name='movies')
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return self.title
