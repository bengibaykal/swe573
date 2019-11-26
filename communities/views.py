from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic.base import TemplateView
from django.core import serializers
from django.urls import reverse
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from .models import Community, Post2, DataTypeObject, DataType, Field

from .forms import PostForm, CommunityForm, CustomForm, DataTypeForm, FieldForm, PostTypeForm
from django.shortcuts import redirect
from django.utils import timezone
import requests
import json
import userdefinedfields
from .serializers import FieldSerializer


from .forms import CustomForm

def index(request):
    communities = Community.objects
    return render(request,'communities/index.html', {'communities': communities})

def specificpost(request, communityId):
    community = Community.objects.get(id=communityId)
    URL = "http://127.0.0.1:8000/api/post/list"
    response = requests.get(URL)
    data = response.json()
    #idcom = response.json()[0]["communityId"]
    #idcom = json.dumps(idcom)
    #idcom = json.loads(idcom)
    data = [x for x in data if x['communityId'] == communityId]
    print(data)
    return render(request, 'communities/specificpost.html', {'data': data, 'communityId': communityId , 'community': community})

def onepost(request, id):
    URL = "http://127.0.0.1:8000/api/post/list"
    response = requests.get(URL)
    data = response.json()
    data = [x for x in data if x['id'] == id]
    print(data)
    return render(request, 'communities/onepost.html', {'data': data, 'id':id})


def post_new(request, communityId):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.modified_by = request.user
            post.communityId = Community.objects.get(id = communityId)
            post.save()
            print(post)
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'communities/post_edit.html', {'form': form, 'communityId': communityId})


def jsonform(request):
    if request.method == "POST":
        query = CustomForm(request.POST)
        if query.is_valid():
            print('--------------------------')
            # With this line, it transforms the form from HTML to JsonSchema
            cleaned_query = query.cleaned_data['data_type']
            print(cleaned_query)
            data_type_object = DataType()
            community = Community.objects.get(name='Universe')
            data_type_object.community = community

            data_type_object.name = cleaned_query['Data Field Name']
            data_type_object.extra_fields = cleaned_query['Data Field Type']
            if cleaned_query['is required'] == "True":
                data_type_object.required = True
            else:
                data_type_object.required = False
            data_type_object.save()

            return print('success')
        else:
            form = CustomForm()
    else:
        print("else run")

    return render(request, 'communities/jsonform.html', {'form': CustomForm})

#TODO: Adding files will be corrected. Add media, image files should be corrected.
def newcommunity(request):
    if request.method == "POST":
        form = CommunityForm(request.POST )
        if form.is_valid():
            community = form.save(commit=False)
            #if 'image' in request.FILES:
                #community.picture = request.FILES['image']

            community.save()
            print(community)
            return redirect('index')
    else:
        form = CommunityForm()
    return render(request, 'communities/newcommunity.html', {'form': form})

#TODO:community search
def search(request, searchtext):

        URL = "http://127.0.0.1:8000/api/post/community?search={}".format(searchtext)
        response = requests.get(URL)
        data = response.json()

        print(data)
        return render(request, 'communities/onepost.html', {'data': data, 'id': id})


class TestDashboardView(TemplateView):
    template_name = 'communities/test.html'

########



def detail(request, Community_id):
    Community_detail = get_object_or_404( Community, pk=Community_id)
    post = Post.objects
    Post.objects.all()
    Communities = Community.objects
    return render(request, 'communities/detail.html',  {'community': Community_detail,'post': post, 'Communities': Communities})


def data_type_creation(request, communityId):

    if request.method == "POST":

        form = DataTypeForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.communityId = Community.objects.get(id = communityId)
            post.save()
            print(post)
            return redirect('index')
    else:
        form = DataTypeForm()
    return render(request, 'communities/newdatatype.html', {'form': form, 'communityId': communityId})

def field_creation(request, communityId, datatypeId):

    if request.method == "POST":
        #datatypeform = DataTypeForm(request.POST)
        form = FieldForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #post.community = Community.objects.get(id = communityId)
            #post.data_type = DataType.objects.get(id = datatypeId)
            print(post)
            post.save()

            Datatype1 = DataType()
            #DataType1 = DataType.objects.get(id = post.data_type)
            #data  = FieldSerializer(post).data
            #print(data)
            #data2 = JsonResponse(data)
            #print(data2)
            URL = "http://127.0.0.1:8000/api/post/field/2"
            response = requests.get(URL)
            data2 = response.json()
            #print(data2)
            community = Community.objects.get(id=communityId)
            com = Community()
            print(community.id)
            datatype = DataType.objects.get(id=datatypeId)
            data = [x for x in data2 if ( x['data_type'] == 15 and x['community'] == community.id)]
            print(data)
            #Datatype1 = DataType1.objects.get(id = datatypeId)

            Datatype1.community = community
            Datatype1.extra_fields = data
            Datatype1.save()
            return redirect('index')
    else:
        form = FieldForm()
    return render(request, 'communities/test.html', {'form': form, 'communityId': communityId, 'datatypeId': datatypeId })

def post_edit(request, id):
    post = get_object_or_404(Post2, id=id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.modified_by = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm(instance=post)
    return render(request, 'communities/post_edit.html', {'form': form})

def datatype_list(request, id):
    datatypes = DataType.objects.filter(community = id)
    #extra_field = json.loads(datatypes.extra_fields)
    community = Community.objects.get(id=id)
    print(datatypes)
    return render(request, 'communities/datatype_list.html', {'datatypes': datatypes , 'community':community})

#TODO: Create JSON Based Form Entry
def post_form_creation(request, communityId, datatypeId):
    form = PostTypeForm(request.POST)
    post = form
    post.modified_by = request.user
    post.communityId = Community.objects.get(id=communityId)
    #print(post)
    community = Community.objects.get(id=communityId)
    datatype = DataType.objects.get(id=datatypeId)
    extrafields = datatype.extra_fields
    name = extrafields['name']
    print(name)
    return render(request, 'communities/postformcreation.html', { 'form': form, 'community': community, 'datatype': datatype, 'name':name})



##########


def post_update(request):
    form = 'Posts Update'
    return HttpResponse(form)

def post_delete(request):
    form = 'Posts Delete'
    return HttpResponse(form)





def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'communities/post_detail.html', {'post': post})

def post_list(request):
    posts = get_object_or_404(Post, pk=pk)
    return render(request, 'communities/post_list.html', {'posts': posts})

#api deneme
def home(request):
    response = requests.get('http://127.0.0.1:8000/api/post/list')
    data = response.json()
    print(data)
    return render(request, 'communities/home.html', {'data': data})



