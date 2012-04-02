from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DjangoBlog.views.home', name='home'),
    # url(r'^DjangoBlog/', include('DjangoBlog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^blog/', include('DjangoBlog.blog.urls')),

)

# for about me
urlpatterns += patterns('',
    url(r'^aboutme/$', 'DjangoBlog.views.aboutme'),
)

# for heroku
import settings
import os

if 'DATABASE_URL' in os.environ:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )


# # for flatpages
# urlpatterns += patterns('',
#     url(r'', include('django.contrib.flatpages.urls')),
# )
