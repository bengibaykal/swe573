from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, RetrieveUpdateAPIView, CreateAPIView


from communities.models import Post2, Community
from communities.api.serializers import Post2Serializer, Post2UpdateCreateSerializer, CommunitySerializer
from rest_framework.permissions import (IsAuthenticated, IsAdminUser)
#custom permission isowner
from communities.api.permissions import IsOwner
from rest_framework.response import Response

#create form from serializer
from django.shortcuts import get_object_or_404

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

import django_filters

from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import render


class DynamicSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])

#TODO:search only on content and topic
class PostListAPIView(ListAPIView):
    queryset = Post2.objects.all()
    serializer_class = Post2Serializer
    filter_backends = [ SearchFilter, OrderingFilter]
    #filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['content']
    search_fields = ['communityId__id']
    lookup_field = 'slug'

class PostDetailAPIView(ListAPIView):
    queryset = Post2.objects.all()
    serializer_class = Post2Serializer
    filter_backends = [DynamicSearchFilter]
    search_fields = ['id']
    lookup_field = 'slug'


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post2.objects.all()
    serializer_class = Post2Serializer
    lookup_field = 'slug'
    #permission_classes = [IsOwner]


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post2.objects.all()
    serializer_class = Post2UpdateCreateSerializer
    lookup_field = 'slug'
    #permission_classes = [IsOwner]

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)


class PostCreateAPIView(CreateAPIView):
    queryset = Post2.objects.all()
    serializer_class = Post2UpdateCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#deneme
class Post2FormDetail(RetrieveAPIView):
    queryset = Post2.objects.all()
    serializer_class = Post2Serializer
    renderer_classes = [TemplateHTMLRenderer]
    #lookup_field = 'slug'
    template_name = 'post2formdetail.html'

#bozuk
class FormCreate(APIView):
    queryset = Post2.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'communities/post2formdetail.html'


    def get(self, request):
        serializer = FormCreate()
        return Response({'serializer': serializer})
        #return render(request, 'post2formdetail.html', {'serializer': serializer, 'style': self.style})


class CommunityListAPIView(ListAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    filter_backends = [ SearchFilter, OrderingFilter ]
    search_fields = ['name', 'summary']
    lookup_field = 'slug'






