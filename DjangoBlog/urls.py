from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from django.template.response import TemplateResponse

class TextResponse(TemplateResponse):
    def __init__(self, *args, **kwargs):
        kwargs['mimetype'] = 'text/plain'
        return super(TextResponse, self).__init__(*args, **kwargs)

# ----------------------------------------------------------------------

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^blog/', include('blog.urls')),
    url(r'^$', include('blog.urls')),
    url(r'^blog/xmlrpc/', include('xmlrpc.urls')),

    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', response_class=TextResponse)),
)

# ----------------------------------------------------------------------

# for heroku
import settings
import os

if 'DATABASE_URL' in os.environ or 'VCAP_SERVICES' in os.environ:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

