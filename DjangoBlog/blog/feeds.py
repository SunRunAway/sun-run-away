from django.contrib.syndication.views import Feed
from blog.models import Blog, Category


class LastEntriesFeeds(Feed):

    def __call__(self, request, *args, **kwargs):
        response = super(LastEntriesFeeds, self).__call__(request, *args, **kwargs)
        response['Content-Type'] = "application/rss+xml; charset=utf-8"
        return response

    title = "Sun Run Away"
    link = "/"
    description = "Invite me when you need me, I will help."

    def items(self):
        return Blog.objects.all()[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_categories(self, item):
        return tuple(item.category.values_list('title', flat=True))

    def item_pubdate(self, item):
        return item.posted

    def categories(self):
        return Category.objects.all()
