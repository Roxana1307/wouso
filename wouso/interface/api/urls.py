__author__ = 'alex'

from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import OAuthAuthentication
from wouso.core.game import get_games

from handlers import NotificationsHandler, InfoHandler
from authentication import SessionAuthentication

# needed by oauth
urlpatterns = patterns(
    'piston.authentication',
    url(r'^oauth/request_token/$','oauth_request_token'),
    url(r'^oauth/authorize/$','oauth_user_auth'),
    url(r'^oauth/access_token/$','oauth_access_token'),
)
urlpatterns += patterns(
    'wouso.interface.api.views',
    url(r'^oauth/request_token_ready/$', 'request_token_ready'),
)

# API:
sessionauth = SessionAuthentication()
authoauth = OAuthAuthentication(realm='Wouso')
ad = {'authentication': [authoauth, sessionauth]}

notifications_resource = Resource(handler=NotificationsHandler, **ad)

urlpatterns += patterns('',
    url(r'^notifications/(?P<type>[^/]+)/$', notifications_resource),
    url(r'^info/$', Resource(handler=InfoHandler, **ad)),
)

for g in get_games():
    api = g.get_api()
    if api:
        for k, v in api.iteritems():
            resource = Resource(handler=v, **ad)
            urlpatterns += patterns('', url(k, resource))