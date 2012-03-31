from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'blog.views.index'),
    url(r'^blog/page/(?P<page>\d+)/$', 'blog.views.index', name='view_blog_page'),

    url(
        r'^blog/view/(?P<slug>.+)/$',
        'blog.views.view_post',
        name='view_blog_post'
    ),

    url(
        r'^blog/category/(?P<slug>.+)/page/(?P<page>\d+)/$',
        'blog.views.view_category',
        name='view_blog_category_page'
    ),
    url(
        r'^blog/category/(?P<slug>.+)/$',
        'blog.views.view_category',
        name='view_blog_category'
    ),

)

# for RSS
from blog.feeds import LastEntriesFeeds
urlpatterns += patterns('',
    url(r'^feeds/$', LastEntriesFeeds()),
)

# for heroku
import settings
import os

if 'DATABASE_URL' in os.environ:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
