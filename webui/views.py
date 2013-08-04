
import datetime
import hashlib
import os
import random
import re

import json

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response, RequestContext
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound

from core.models import Cover, Episode, Genre, Hardlink, Inode, Season, TVShow


@login_required
def episode(request, tvshow, episode):
    tvshow = TVShow.objects.get(pk=tvshow)
    episode = Episode.objects.get(tvshow=tvshow, pk=episode)

    return render_to_response('webui/player.html',
        {'object': episode})

@login_required
def genre(request, genre):
    genre = Genre.objects.get(pk=genre)

    return render_to_response('webui/genre.html',
        {'genre': genre})

def index(request):
    try:
        nexturl = request.GET['next']
    except:
        nexturl = '/tvshows.html'

    if request.user.is_authenticated():
        return redirect(nexturl)
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(nexturl)
                else:
                    return render_to_response('webui/login.html',
                        {'error': 'inactive'},
                        context_instance=RequestContext(request))
            else:
                return render_to_response('webui/login.html',
                    {'error': 'wrongpass'},
                    context_instance=RequestContext(request))
        else:
            return render_to_response('webui/login.html',
                {},
                context_instance=RequestContext(request))

@login_required
def tvshow(request, tvshow):
    tvshow = TVShow.objects.get(pk=tvshow)
    seasons = Season.objects.filter(tvshow=tvshow).order_by('season')

    return render_to_response('webui/tvshow.html',
        {'tvshow': tvshow, 'seasons': seasons})

@login_required
def tvshows(request):
    genres = Genre.objects.all()

    return render_to_response('webui/tvshows.html',
        {'genres': genres})
