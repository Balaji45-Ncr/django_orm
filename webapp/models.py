from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User
# Create your models here.
class STATUS(models.TextChoices):
    Draft='0',_('Draft')
    Publish='1',_('Publish')
    Archive='2',_('Archive')

class Category(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(max_length=200,null=True,blank=True)

class Post(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    title=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200)
    summary=models.CharField(max_length=200,null=True,blank=True)
    status=models.CharField(max_length=1,choices=STATUS.choices,default=STATUS.Draft)
    image=models.ImageField(upload_to='post',default=None)
    category=models.ManyToManyField(Category,related_name='posts')
    views=models.IntegerField(default=0)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    author=models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE)
    text=models.TextField(max_length=500)
    approved_comment=models.BooleanField(default=False)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')
