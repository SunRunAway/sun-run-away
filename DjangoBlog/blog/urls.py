from django.conf.urls.defaults import patterns, url
from DjangoBlog import settings
urlpatterns = patterns('',
    url(r'^$', 'blog.views.index'),
    url(r'^page/(?P<page>\d+)/$', 'blog.views.index'),

    url(
        r'^blog/view/(?P<slug>.+)/$',
        'blog.views.view_post',
        name='view_blog_post'
    ),

    url(
        r'^blog/category/(?P<slug>.+)/page/(?P<page>\d+)/$',
        'blog.views.view_category',
    ),
    url(
        r'^blog/category/(?P<slug>.+)/$',
        'blog.views.view_category',
        name='view_blog_category'
    ),

)

import os
if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
