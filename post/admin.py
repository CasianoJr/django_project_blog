from django.contrib import admin
from .models import Category, Post, Comment, ChildComment, Image


class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title',
                    'slug', 'date_created']
    list_filter = ['title']
    list_editable = ['slug']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(ChildComment)
admin.site.register(Image)