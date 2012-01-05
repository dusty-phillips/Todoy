from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^accounts/login/$', 'todoy.register.views.login'),
    url(r'^accounts/register/$', 'todoy.register.views.register'),
    url(r'^accounts/logout/$', 'todoy.register.views.logout'),

    url(r'^$', 'todoy.todos.views.index', name='index'),
    url(r'^home/(?P<username>[^/]+)/$', 'todoy.todos.views.user_home', name='user_home'),
    url(r'^home/(?P<username>[^/]+)/cache.manifest$', 'todoy.todos.views.user_manifest', name='user_manifest'),
    # url(r'^todoy/', include('todoy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
