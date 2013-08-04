import datetime
import hashlib
import mutagen.mp4
import os
import random
import re

import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound

from core.models import Cover, Episode, Genre, Hardlink, Inode, Season, TVShow


@login_required
def hardlink(request):
    try:
        inode_id = int(request.GET['object'])
    except:
        return HttpResponseBadRequest(content=json.dumps({
            'status': 'error',
            'reason': 'object id required'
        }), content_type='application/json')

    try:
        inode = Inode.objects.get(pk=inode_id)
    except:
        return HttpResponseNotFound(content=json.dumps({
            'status': 'error',
            'reason': 'no object with such id found'
        }), content_type='application/json')

    token = hashlib.sha256()
    token.update('%s:%s:%s:%s:%s' % (inode.path, inode.pk, inode.created, datetime.datetime.now(), random.randrange(1,9999999)))
    token_hex = token.hexdigest()

    hardlink = Hardlink(inode=inode, token=token_hex)
    os.symlink(inode.path, '%s/%s.m4v' % (settings.MEDIAFILES_HARDLINKS, token_hex))
    hardlink.save()

    return HttpResponse(content=json.dumps({
        'status': 'ok',
        'token': token_hex
    }), content_type='application/json')
