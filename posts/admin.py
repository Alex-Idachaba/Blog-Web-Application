from django.contrib import admin
from posts.models import Author, Categories, Comment, Post

admin.site.register(Author)
admin.site.register(Categories)
admin.site.register(Post)
admin.site.register(Comment)
