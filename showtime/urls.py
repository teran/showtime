from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'showtime.views.home', name='home'),
    # url(r'^showtime/', include('showtime.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^$', 'webui.views.index'),
    (r'^tvshows.html$', 'webui.views.tvshows'),
    (r'^genre/(?P<genre>[0-9]+).html$', 'webui.views.genre'),
    (r'^tvshow/(?P<tvshow>[0-9]+).html$', 'webui.views.tvshow'),
    (r'^tvshow/(?P<tvshow>[0-9]+)/(?P<episode>[0-9]+).html$', 'webui.views.episode'),
    #(r'^movies.html$', 'webui.views.movies'),
    #(r'^movie/(?P<id>[0-9]).html$', 'webui.views.movie'),

    (r'^api/hardlink.json$', 'api.views.hardlink'),
)
