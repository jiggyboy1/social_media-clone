from django.contrib import admin
from .models import Post,Profile,Like,Follow,Comment
# Register your models here.

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Like)