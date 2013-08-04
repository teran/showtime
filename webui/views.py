
import datetime
import hashlib
import os
import random
import re

import json

from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound

from core.models import Cover, Episode, Genre, Hardlink, Inode, Season, TVShow


def episode(request, tvshow, episode):
    tvshow = TVShow.objects.get(pk=tvshow)
    episode = Episode.objects.get(tvshow=tvshow, pk=episode)

    return render_to_response('webui/player.html',
        {'object': episode})

def genre(request, genre):
    genre = Genre.objects.get(pk=genre)

    return render_to_response('webui/genre.html',
        {'genre': genre})

def index(request):
    genres = Genre.objects.all()

    return render_to_response('webui/index.html',
        {'genres': genres})

def tvshow(request, tvshow):
    tvshow = TVShow.objects.get(pk=tvshow)
    seasons = Season.objects.filter(tvshow=tvshow).order_by('season')

    return render_to_response('webui/tvshow.html',
        {'tvshow': tvshow, 'seasons': seasons})
