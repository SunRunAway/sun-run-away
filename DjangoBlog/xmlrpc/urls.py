from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'django_xmlrpc.views.handle_xmlrpc', name='xmlrpc'),
)
