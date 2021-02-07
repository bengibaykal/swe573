from rest_framework import serializers
from communities.models import Post2, Post, Community

class Post2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Post2
        fields = [
            'user',
            'title',
            'content',
            'slug',
            'created',
            'modified_by',
            'communityId',
            'id',
        ]

class Post2UpdateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post2
        fields = [
            'title',
            'content',
        ]

#community specific data type
class PostCreateDataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post2
        fields = [
            'newDataType',
        ]
#community specific data type
class DataTypeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'dataTypeName',
            'dataTypeType',
            'dataTypeIsRequired',
        ]

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = [
            'name',
            'summary',
        ]

