# Create your views here.
from blog.models import Blog, Category
from django.shortcuts import render_to_response, get_object_or_404

ARTICLES_PER_PAGE = 5


def index(request, page='1'):
    end = int(page) * ARTICLES_PER_PAGE
    totalPageNum = (Blog.objects.count() + ARTICLES_PER_PAGE - 1) / ARTICLES_PER_PAGE
    return render_to_response('index.html', {
        'categories': Category.objects.all(),
        'posts': Blog.objects.all()[end - ARTICLES_PER_PAGE: end],
        'pageNum': int(page),
        'pageRange': range(totalPageNum),
    })


def view_post(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    try:
        postPrevious = Blog.objects.get(id=post.id - 1)
    except Exception:
        postPrevious = None
    try:
        postNext = Blog.objects.get(id=post.id + 1)
    except Exception:
        postNext = None

    # postPrevious = get_object_or_404(Blog, id=1)
    return render_to_response('view_post.html', {
        'post': post,
        'postPrevious': postPrevious,
        'postNext': postNext,
    })


def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render_to_response('view_category.html', {
        'category': category,
        'posts': Blog.objects.filter(category=category)[:5],
    })
