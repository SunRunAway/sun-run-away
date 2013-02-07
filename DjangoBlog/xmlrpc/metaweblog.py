import urlparse
from datetime import datetime
from xmlrpclib import DateTime
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings
from blog.models import Category, Blog
from xmlrpc.views import public

def authenticated(pos=1):
    """
    A decorator for functions that require authentication.
    Assumes that the username & password are the second & third parameters.
    Doesn't perform real authorization (yet), it just checks that the
    user is_superuser.
    """

    def _decorate(func):
        def _wrapper(*args, **kwargs):
            username = args[pos+0]
            password = args[pos+1]
            args = args[0:pos]+args[pos+2:]
            try:
                user = User.objects.get(username__exact=username)
            except User.DoesNotExist:
                traceback.print_exc()
                raise ValueError("Authentication Failure")
            if not user.check_password(password):
                traceback.print_exc()
                raise ValueError("Authentication Failure")
            if not user.is_superuser:
                traceback.print_exc()
                raise ValueError("Authorization Failure")
            return func(user, *args, **kwargs)

        return _wrapper
    return _decorate

site = Site.objects.get_current()
site_url = 'http://'+site.domain

def full_url(url):
    return urlparse.urljoin(site_url, url)

#--------------------------------------------------

def blog_struct():
    return {
        'blogid': settings.SITE_ID,
        'blogName': site.name,
        'url': site_url,
    }


@authenticated()
def blogger_getUsersBlogs(user, appkey):
    """
    an array of <struct>'s containing the ID (blogid), name
    (blogName), and URL (url) of each blog.
    """
    return [blog_struct()]

#--------------------------------------------------

def category_struct(category):
    struct = {
        'description': str(category.title),
        'htmlUrl': str(full_url(category.get_absolute_url())),
        'rssUrl': '',
    }
    return struct

@authenticated()
def metaWeblog_getCategories(user, blogid):
    p = [category_struct(category)
            for category in Category.objects.all()]
    return p

#--------------------------------------------------

# example... this is what wordpress returns:
# {'permaLink': 'http://gabbas.wordpress.com/2006/05/09/hello-world/',
#  'description': 'Welcome to <a href="http://wordpress.com/">Wordpress.com</a>. This is your first post. Edit or delete it and start blogging!',
#  'title': 'Hello world!',
#  'mt_excerpt': '',
#  'userid': '217209',
#  'dateCreated': <DateTime u'20060509T16:24:39' at 2c7580>,
#  'link': 'http://gabbas.wordpress.com/2006/05/09/hello-world/',
#  'mt_text_more': '',
#  'mt_allow_comments': 1,
#  'postid': '1',
#  'categories': ['Uncategorized'],
#  'mt_allow_pings': 1}

def format_date(d):
    if not d: return None
    return DateTime(d.isoformat())

def post_struct(blog):
    link = full_url(blog.get_absolute_url())
    categories = blog.category.all()
    struct = {
        'postid': blog.id,
        'title': blog.title,
        'link': link,
        'permaLink': link,
        'description': blog.body_markdown,
        'categories': [c.title for c in categories],
        # 'userid': blog.author.id,
        # 'mt_excerpt': '',
        # 'mt_text_more': '',
        # 'mt_allow_comments': 1,
        # 'mt_allow_pings': 1}
        }
    if blog.posted:
        struct['dateCreated'] = format_date(blog.posted)
    return struct

@authenticated()
def metaWeblog_newPost(user, blogid, struct, publish):

    # todo - parse out technorati tags
    post = Blog(title = struct['title'],
                body_markdown = struct['description'],
                posted = datetime.strptime(struct['dateCreated'].value[:18], '%Y-%m-%dT%H:%M:%S'),
                slug = struct.get('permaLink', None),
               )
    post.save()
    setTags(post, struct)
    return post.id

#--------------------------------------------------


def setTags(post, struct):
    tags = struct.get('categories', None)
    if tags is None:
        post.category = []
    else:
        post.category = [Category.objects.get(name__iexact=name) for name in tags]


@authenticated()
def metaWeblog_getPost(user, postid):
    post = Blog.objects.get(id=postid)
    return post_struct(post)


@authenticated()
def metaWeblog_getRecentPosts(user, blogid, num_posts):
    posts = Blog.objects.order_by('-id')[:int(num_posts)]
    return [post_struct(post) for post in posts]

@authenticated()
def metaWeblog_editPost(user, postid, struct, publish):
    post = Blog.objects.get(id=postid)
    title = struct.get('title', None)
    if title is not None:
        post.title = title
    body_markdown = struct.get('description', None)
    if body_markdown is not None:
        post.body_markdown = body_markdown
        # todo - parse out technorati tags
    setTags(post, struct)
    post.save()
    return True


@authenticated(pos=2)
def blogger_deletePost(user, appkey, postid, publish):
    post = Blog.objects.get(id=postid)
    post.delete()
    return True


@authenticated()
def metaWeblog_newMediaObject(user, blogid, struct):
    # The input struct must contain at least three elements, name,
    # type and bits. returns struct, which must contain at least one
    # element, url

    # This method isn't implemented yet, obviously.

    return {}
