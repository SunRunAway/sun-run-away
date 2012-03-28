# Create your views here.
from blog.models import Blog, Category
from django.shortcuts import render_to_response, get_object_or_404
import datetime

ARTICLES_PER_PAGE = 5


def index(request, page='1'):
    end = int(page) * ARTICLES_PER_PAGE
    totalPageNum = (Blog.objects.count() + ARTICLES_PER_PAGE - 1) / ARTICLES_PER_PAGE
    #print Blog.objects.all()[end - ARTICLES_PER_PAGE: end]
    return render_to_response('index.html', {
        'categories': Category.objects.all(),
        'posts': Blog.objects.all()[end - ARTICLES_PER_PAGE: end],
        'pageNum': int(page),
        'pageRange': range(totalPageNum),
        'nowDate': datetime.date.today(),
    })


def view_post(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    try:
        postPrevious = Blog.objects.reverse().filter(id__lt=post.id)[0]
    except IndexError:
        postPrevious = None

    try:
        postNext = Blog.objects.filter(id__gt=post.id)[0]
    except IndexError:
        postNext = None

    return render_to_response('view_post.html', {
        'post': post,
        'postPrevious': postPrevious,
        'postNext': postNext,
        'categories': Category.objects.filter(blog=post)
    })


def view_category(request, slug, page='1'):
    print(slug, page)
    category = get_object_or_404(Category, slug=slug)
    blogsFromCategory = Blog.objects.filter(category=category)
    end = int(page) * ARTICLES_PER_PAGE
    totalPageNum = (len(blogsFromCategory) + ARTICLES_PER_PAGE - 1) / ARTICLES_PER_PAGE
    return render_to_response('view_category.html', {
        'category': category,
        'posts': blogsFromCategory[end - ARTICLES_PER_PAGE: end],
        'pageNum': int(page),
        'pageRange': range(totalPageNum),
    })
