from django.contrib.syndication.views import Feed
from blog.models import Blog

class LastEntriesFeeds(Feed):
    title = "Sun Run Away"
    link = "/blog/view/"
    description = "Get rss feeds from my blog"

    def items(self):
        return Blog.objects.all()[:5]

    def item_title(self, item):
        return item.title
