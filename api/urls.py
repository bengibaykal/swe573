from django.urls import path
from django.urls import include
from communities.api.views import CommunityListAPIView, FormCreate, PostListAPIView, PostDetailAPIView, PostDeleteAPIView, PostUpdateAPIView, PostCreateAPIView, Post2FormDetail


urlpatterns = [

    path('list/', PostListAPIView.as_view(), name = 'list'),
    path('detail/', PostDetailAPIView.as_view(), name ='detail'),
    path('update/<slug>', PostUpdateAPIView.as_view(), name = 'update'),
    path('delete/<slug>', PostDeleteAPIView.as_view(), name = 'delete'),
    path('create/', PostCreateAPIView.as_view(), name = 'create'),

    path('community/', CommunityListAPIView.as_view(), name='community'),

    path('form/', FormCreate.as_view(), name='FormCreate'),

]
