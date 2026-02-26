from django.contrib import admin
from .models import Category,Post,Like_post

# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Like_post)

