from django.contrib.syndication.views import Feed
from blog.models import Blog, Category


class LastEntriesFeeds(Feed):
    title = "Sun Run Away"
    link = "/"
    description = "Get rss feeds from my blog"

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
