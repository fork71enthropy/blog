from django.contrib import admin
from .models import Profile,Author,Project,Book

# Register your models here.
admin.site.register(Profile)
admin.site.register(Author)
admin.site.register(Project)
admin.site.register(Book)
