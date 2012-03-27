from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
import datetime


# Create your models here.
class Blog (models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, null=True, unique=True)
    body = models.TextField()
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    category = models.ForeignKey("blog.Category", null=True)

    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ("view_blog_post", None, {"slug": self.slug})

    def save(self):
        super(Blog, self).save()
        date = datetime.date.today()
        self.slug = '%i/%i/%i/%s' % (
            date.year, date.month, date.day, slugify(self.title)
        )
        super(Blog, self).save()


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ("view_blog_category", None, {"slug": self.slug})
