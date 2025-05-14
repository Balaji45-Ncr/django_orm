from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
# Create your views here.
from .serializers import (CategorySerializers,CommentSerializers,LikeSerializers,PostSerializers)
from .models import Category,Comment,Like,Post
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    @action(detail=False,methods=['POST'])
    def create_data(self,request,*args,**kwargs):
        data=self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        title=data.validated_data['title']
        slug = data.validated_data['slug']
        description = data.validated_data['description']
        model_data=Category.objects.create(title=title,slug=slug,description=description)
        serialize=self.serializer_class(model_data)
        return Response(serialize.data,status=status.HTTP_201_CREATED)

    @action(detail=False,methods=['POST'])
    def save_data(self,request,*args,**kwargs):
        data=self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        title_data=data.validated_data.get('title')
        slug_data=data.validated_data.get('slug')
        description_data=data.validated_data.get('description')
        obj=Category(title=title_data,slug=slug_data,description=description_data)
        obj.save()
        serializer=self.serializer_class(obj)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    @action(detail=False,methods=['POST'])
    def get_or_create_data(self,request,*args,**kwargs):
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        title_data = data.validated_data.get('title')
        slug_data = data.validated_data.get('slug')
        description_data = data.validated_data.get('description')
        obj,_=Category.objects.get_or_create(title=title_data,slug=slug_data)
        serializers=self.serializer_class(obj)
        return Response(serializers.data,status=status.HTTP_201_CREATED)



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializers

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
