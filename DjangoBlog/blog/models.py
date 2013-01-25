from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
from django.utils.http import urlquote
import datetime
import markdown

# Create your models here.
class Blog (models.Model):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    body_markdown = models.TextField('Entry body', help_text='Use Markdown syntax.')
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
        if self.posted:
            date = self.posted.date()
        else:
            date = datetime.date.today()
        prefix = '%i/%i/%i/' % (
            date.year, date.month, date.day
        )
        if self.slug.startswith(prefix):
            self.slug = self.slug[len(prefix):]
        self.slug = prefix + slugify(urlquote(self.slug))

        if self.body_markdown:
            self.body = markdown.markdown(self.body_markdown)
        super(Blog, self).save()


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ("view_blog_category", None, {"slug": self.slug})
