#!/usr/bin/env python

import datetime
import hashlib
import os
import re
from PIL import Image
import subprocess
import tempfile
import time

import json

import mutagen.mp4

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "showtime.settings")

from django.conf import settings
from django.template.defaultfilters import slugify

from core.models import Cover, Episode, Genre, Hardlink, Inode, Season, TVShow

if __name__ == "__main__":
    cmd = "/usr/bin/find %s -name '*.m4v' -or -name '*.mp4'" % " ".join(settings.MEDIAFILES_DIR)
    print "Running %s" % cmd
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    p.wait()

    files = stdout.split("\n")

    mp4search = re.compile('\.(mp4|m4v)$')
    for filename in files:
        print "Working on %s" % filename
        if mp4search.search(filename):
            #try:
            meta = mutagen.mp4.MP4(filename)
            #except:
            #    print "Error obtaining meta data from %s. Skipping" % filename
            #    continue

            try:
                tvshow, tvshow_created = TVShow.objects.get_or_create(title=meta['tvsh'][0])
            except:
                tvshow, tvshow_created = TVShow.objects.get_or_create(title='Unknown')



            inode, inode_created = Inode.objects.get_or_create(path=filename)

            if inode_created:
                inode.path = filename
                inode.save()

            try:
                episode, episode_created = Episode.objects.get_or_create(
                    title=meta['\xa9nam'][0],
                    tvshow=tvshow, inode=inode)
            except:
                continue

            #try:
            cover_data = meta['covr'][0]

            digest = hashlib.sha1()
            digest.update(cover_data)

            cover, cover_created = Cover.objects.get_or_create(digest=digest.hexdigest())

            if cover_created:
                fp = open('%s/%s.jpg' % (settings.COVERS_DIR, cover.digest), 'w')
                fp.write(cover_data)
                fp.close()
                image = Image.open('%s/%s.jpg' % (settings.COVERS_DIR, cover.digest))
                image.thumbnail((200, 200), Image.ANTIALIAS)
                image.save('%s/%s-preview.jpg' % (settings.COVERS_DIR, cover.digest), 'JPEG')
                cover.save()

            tvshow.cover = cover
            episode.cover = cover

            try:
                episode.episode = meta['trkn'][0][0]
            except:
                pass

            try:
                season, season_created = Season.objects.get_or_create(tvshow=tvshow, season=meta['tvsn'][0])

                if season_created:
                    season.cover = cover

                season.save()
                episode.season = season
            except:
                pass

            genre, genre_created = Genre.objects.get_or_create(name=meta['\xa9gen'][0])
            genre.save()
            tvshow.genre = genre

            if tvshow_created:
                tvshow.save()

            episode.slug = slugify(episode.title)
            if episode_created:
                episode.save()

    hardlinks = Hardlink.objects.filter(created__lt = (datetime.datetime.now() - datetime.timedelta(minutes = 10)))
    for hardlink in hardlinks:
        os.unlink('%s/%s.m4v' % (settings.MEDIAFILES_HARDLINKS, hardlink.token))
        hardlink.delete()