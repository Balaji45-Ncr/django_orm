from django.contrib import admin
from .models import Category,Post,Comment,Like
# Register your models here.

class Postadmin(admin.ModelAdmin):
    list_display = ['author','title','views']

class Categoryadmin(admin.ModelAdmin):
    list_display = ['title','slug']
#admin.site.register(Post)
admin.site.register(Post,Postadmin)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Category,Categoryadmin)
