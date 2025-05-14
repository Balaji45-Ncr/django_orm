from .models import Post,Category,Comment,Like

from rest_framework import serializers

class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields='__all__'

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields='__all__'

class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model=Like
        fields='__all__'
