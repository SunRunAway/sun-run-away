from django.contrib import admin
from blog.models import Blog, Category


class BlogAdmin(admin.ModelAdmin):
    exclude = ['slug']
    prepopulated_fields = {'slug': ('title', )}


class BlogCategory(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Blog)
admin.site.register(Category)
