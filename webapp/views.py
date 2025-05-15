from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
# Create your views here.
from .serializers import (CategorySerializers,CommentSerializers,LikeSerializers,PostSerializers)
from .models import Category,Comment,Like,Post,STATUS
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

    @action(detail=True,methods=['PATCH'])
    def add_category(self,request,pk,*args,**kwargs):
        category=request.data.get('ids')
        instance=Post.objects.filter(pk=pk).first()

        category=set(category)
        instance.category.add(*category)

        serializer=self.serializer_class(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(detail=True,methods=['POST'])
    def set_category(self,request,pk,*args,**kwargs):
        request_browser = request.data.get('data_id')
        try:
            # request_browser=request.data.get('data_id')
            database=Post.objects.filter(pk=pk).first()
            #database.category.clear()
            database.category.set(request_browser)
            serializer=self.serializer_class(database)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except :
            return Response(status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True,methods=['POST'])
    def update_data(self,request,pk,*args,**kwargs):
        summary_data=request.data.get('summary')
        content_data=request.data.get('content')

        db_data=Post.objects.filter(pk=pk).update(summary=summary_data,content=content_data)
        serializer=self.serializer_class(db_data)
        return Response({'message':'Successfully updated the data'})
    @action(detail=False,methods=['POST'])
    def update_or_create_method(self,request,*args,**kwargs):
        summary_data = request.data.get('summary')
        content_data = request.data.get('content')
        title_data = request.data.get('title')
        category_data = set(request.data.get('category'))
        author=1
        obj,_=Post.objects.update_or_create(

            title=title_data,
            defaults={
                'summary':summary_data,
                'content':content_data,
                'author.id':author,
            }
        )
        obj.category.add(*category_data)
        return Response({'message': 'Successfully updated the data'})

    @action(detail=False, methods=['POST'])
    def bulk_update_method(self, request, *args, **kwargs):
        ids = request.data.get("ids")

        # ✅ Check if IDs exist
        if not ids:
            return Response(
                {"error": "Missing or empty 'ids' list."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Check if it's a list
        if not isinstance(ids, list):
            return Response(
                {"error": "'ids' must be a list of integers."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Optional: Ensure all values are integers
        try:
            ids = list(map(int, ids))
        except ValueError:
            return Response(
                {"error": "All values in 'ids' must be integers."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Now safe to query
        queryset = Post.objects.filter(id__in=ids)

        for post in queryset:
            post.status = STATUS.Publish.value

        Post.objects.bulk_update(queryset, ['status'])

        return Response(
            {"message": f"Updated {len(queryset)} post(s) successfully."},
            status=status.HTTP_200_OK
        )






