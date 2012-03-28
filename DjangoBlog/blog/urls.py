from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'blog.views.index'),
    url(r'^page/(?P<page>\d+)/$', 'blog.views.index'),
    url(
        r'^blog/view/(?P<slug>[^\.]+).html',
        'blog.views.view_post',
        name='view_blog_post'
    ),
    url(
        r'^blog/category/(?P<slug>[^\.]+).html',
        'blog.views.view_category',
        name='view_blog_category'
    ),

)