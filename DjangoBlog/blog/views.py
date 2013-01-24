# Create your views here.
from blog.models import Blog, Category
from django.template import RequestContext
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import permalink
import datetime

ARTICLES_PER_PAGE = 5


def index(request, page='1'):
    page = int(page)
    entryEnd = page * ARTICLES_PER_PAGE
    entryBegin = entryEnd - ARTICLES_PER_PAGE
    entryTotal = Blog.objects.count()
    if entryTotal < entryEnd:
        entryEnd = entryTotal

    if entryBegin > entryTotal:
        raise Http404

    totalPageNum = (entryTotal + ARTICLES_PER_PAGE - 1) / ARTICLES_PER_PAGE

    @permalink
    def get_absolute_url(page):
        return ("view_blog_page", None, {"page": page})

    return render_to_response('index.html', {
        'allCategories': Category.objects.all(),    # for navigation
        'nowDate': datetime.date.today(),           # for banner's date


        'posts': Blog.objects.all()[entryBegin: entryEnd],

        'entryBegin': entryBegin + 1,               # for pager info
        'entryEnd': entryEnd,
        'entryTotal': entryTotal,

        'pagePrevious': get_absolute_url(page - 1) if page > 1 else None,           # for pager converter
        'pageNext': get_absolute_url(page + 1) if page < totalPageNum else None,
    }, context_instance=RequestContext(request))


def view_post(request, slug):
    post = get_object_or_404(Blog, slug=slug)

    try:
        postPrevious = Blog.objects.reverse().filter(id__gt=post.id)[0]
    except IndexError:
        postPrevious = None

    try:
        postNext = Blog.objects.filter(id__lt=post.id)[0]
    except IndexError:
        postNext = None
    print(post, postNext, postPrevious)
    return render_to_response('view_post.html', {
        'allCategories': Category.objects.all(),    # for navigation

        'post': post,
        'categories': Category.objects.filter(blog=post),

        'noNeedDash': True,                         # for pager info
        'entryEnd': Blog.objects.filter(id__gt=post.id).count() + 1,
        'entryTotal': Blog.objects.count(),

        'pagePrevious': postPrevious.get_absolute_url() if postPrevious else None,      # for pager converter
        'pageNext': postNext.get_absolute_url() if postNext else None,

    }, context_instance=RequestContext(request))


def view_category(request, slug, page='1'):
    page = int(page)
    category = get_object_or_404(Category, slug=slug)
    blogsFromCategory = Blog.objects.filter(category=category)

    entryEnd = int(page) * ARTICLES_PER_PAGE
    entryBegin = entryEnd - ARTICLES_PER_PAGE
    entryTotal = blogsFromCategory.count()
    if entryTotal < entryEnd:
        entryEnd = entryTotal

    if entryBegin > entryTotal:
        raise Http404

    totalPageNum = (entryTotal + ARTICLES_PER_PAGE - 1) / ARTICLES_PER_PAGE

    @permalink
    def get_absolute_url(slug, page):
        return ("view_blog_category_page", None, {"slug": slug, "page": page})

    return render_to_response('view_category.html', {
        'allCategories': Category.objects.all(),    # for navigation

        'category': category,
        'posts': blogsFromCategory[entryBegin: entryEnd],

        'entryBegin': entryBegin + 1,               # for pager info
        'entryEnd': entryEnd,
        'entryTotal': entryTotal,

        'pagePrevious': get_absolute_url(slug, page - 1) if page > 1 else None,           # for pager converter
        'pageNext': get_absolute_url(slug, page + 1) if page < totalPageNum else None,
    }, context_instance=RequestContext(request))
