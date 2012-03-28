from django.contrib import admin
from blog.models import Blog, Category


class BlogAdmin(admin.ModelAdmin):
    fields = ('title', 'body', 'category')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
