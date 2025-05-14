from django.urls import path
from . import views  # Or from webapp import views
from rest_framework.routers import DefaultRouter


routers=DefaultRouter()
routers.register('categories',views.CategoryViewSet,basename='category')
routers.register('posts',views.PostViewSet,basename='post')
urlpatterns =  routers.urls

