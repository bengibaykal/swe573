from django.urls import path

from .import views
from .views import post_new, post_edit, post_detail, post_list, specificpost , jsonform, newcommunity
from django.urls import include


#import the same level files

urlpatterns = [
    path('',views.index,name = "index"),
    path('allposts/<int:communityId>', views.specificpost, name='specificpost'),
    path('post/new/<int:communityId>', post_new, name='post_new'),
    path('onepost/<int:id>', views.onepost, name='onepost'),
    path('jsonform/', views.jsonform, name='jsonform'),
    path('newcommunity/' , newcommunity , name='newcommunity'),
    path('search/?search=<searchtext>' , views.search , name='search'),

    path('home', views.home, name='home'),
    path('api/post/', include('communities.api.urls')),

    path('post/<int:id>/edit/', post_edit, name='post_edit'),
    path('<int:Community_id>',views.detail,name = "detail"),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/list', post_list, name='post_list'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),



]
