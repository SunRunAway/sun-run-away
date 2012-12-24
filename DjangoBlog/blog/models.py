from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
from django.utils.http import urlquote
import datetime


# Create your models here.
class Blog (models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, null=True, unique=True)
    body = models.TextField()
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    category = models.ManyToManyField("blog.Category", null=True)

    class Meta:
        ordering = ['-id']  # or '-posted'?

    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ("view_blog_post", None, {"slug": self.slug})

    def save(self):
        #super(Blog, self).save()
        if self.posted:
            date = self.posted.date()
        else:
            date = datetime.date.today()
        self.slug = '%i/%i/%i/%s' % (
            date.year, date.month, date.day, slugify(urlquote(self.title))
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
