from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic.base import TemplateView
from django.core import serializers
from django.urls import reverse
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from .models import Community, Post2, DataTypeObject, DataType, Field
from django.core.serializers import serialize

from .forms import PostForm, CommunityForm, CustomForm, DataTypeForm, FieldForm, PostTypeForm
from django.shortcuts import redirect
from django.utils import timezone
import requests
import json
import userdefinedfields
from .serializers import FieldSerializer
from django.core.serializers.json import DjangoJSONEncoder



from .forms import CustomForm

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, json):
            return str(obj)
        return super().default(obj)

def index(request):
    communities = Community.objects
    return render(request,'communities/index.html', {'communities': communities})

def specificpost(request, communityId):
    community = Community.objects.get(id=communityId)
    URL = "http://127.0.0.1:8000/api/post/list"
    response = requests.get(URL)
    data = response.json()
    data = [x for x in data if x['communityId'] == communityId]
    print(data)
    dto = DataTypeObject.objects.filter( community = community )
    print(dto)




    return render(request, 'communities/specificpost.html', {'data': data, 'communityId': communityId , 'community': community , 'dto' : dto })

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



    return render(request, 'communities/jsonform.html', {'form': CustomForm()})


#DONE
def newcommunity(request):
    if request.method == "POST":
        form = CommunityForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            community = form.save(commit=False)
            if 'image' in request.FILES:
                community.image = request.FILES['image']
            community.save()

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

def datatypefields(request, datatypeId):
    myDict = {}

    f = {}


    #DataType1 = get_object_or_404(DataType, pk=datatypeId)
    DataType1 = DataType.objects.filter(id=datatypeId)
    community2 = DataType.objects.get(id=datatypeId).community

    #print(community2)

    community = Community.objects.get(id = community2)
    datatype = DataType.objects.get(id = datatypeId)
    #print(community)

    print(DataType1)
    DataType.objects.all()
    Field1 = Field.objects.filter(data_type=datatypeId)


    DataTypeObject1 = DataTypeObject()
    DataTypeObject1.community = community
    DataTypeObject1.data_type = datatype


    #print(DataTypeObject1)
    if (request.method == "POST"):
        myDict = {}

        # saves as key:value pairs but does not work so changed as below
        #for key in queryDict:
        #    myDict[key] = request.POST[key]
        #print(myDict)
        # DataTypeObject1.save()
        # print(DataTypeObject1)

        query = request.POST
        _mutable = query._mutable
        query._mutable = True
        del query['csrfmiddlewaretoken']
        query._mutable = False
        queryDict = query.keys()


        f = {}
        f['fields'] = []
        for key in queryDict:
          myDict= {  'name': key,
                   'value' :   request.POST[key],
              }

          f['fields'].append(myDict)
        DataTypeObject1.fields = f
        DataTypeObject1.save()
        print(DataTypeObject1)

        #value = myDict.values()

    return render(request, 'communities/datatypefields.html',
                  { 'DataType': DataType1, 'Field': Field1, 'Allfields': myDict , 'fields': f })




def field_creation(request, communityId, datatypeId):
    #field = DataType.objects.get(id=2)
    #field_extra = field['extra_fields']

    if request.method == "POST":

        #datatypeform = DataTypeForm(request.POST)
        form = FieldForm(request.POST)
        print(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            Community1 = Community.objects.get(id = communityId)
            DT1 = DataType.objects.get(id = datatypeId)
            post.community = Community1
            post.data_type = DT1
            #post.required = request.POST.required
            #print(post.required)

            post.save()
            print(post.name)

            DataType1 = DataType.objects.get(pk=post.data_type_id)
            # data  = FieldSerializer(post).data
            # print(data)
            # data2 = JsonResponse(data)
            # print(data2)
            URL = "http://127.0.0.1:8000/api/post/field/2"
            response = requests.get(URL)
            data2 = response.json()
            print(data2)
            data = [x for x in data2 if (x['community'] == communityId and x['data_type'] == datatypeId)]
            print(data)
            DataType1.extra_fields = data
            DataType1.save()
            return redirect('index')
    else:
        form = FieldForm()
    return render(request, 'communities/test.html',
                  {'form': form, 'communityId': communityId, 'datatypeId': datatypeId})

def field_creation2(request, communityId, datatypeId):
    myDict = {}
    Community1 = Community.objects.get(id=communityId)
    DT1 = DataType.objects.get(id=datatypeId)

    if (request.method == "POST"):
        queryDict = request.POST.keys()
        queryDict2 = queryDict

        print(queryDict2)
        myDict = {}
        for key in queryDict:
            myDict[key] = request.POST[key]
        myDict['community'] = communityId
        myDict['data_type'] = datatypeId
        print(myDict)
        del myDict['csrfmiddlewaretoken']
        print(myDict)
        #DT1.extra_fields = myDict
        existing_fields = DT1.extra_fields


        #DT1.extra_fields == {}:
        #existing_field

        #d1 = DT1.extra_fields
        #print(d1)
        #d2 = dict((list(d1.items())) + list(myDict.items()))
        #print("d2")
        #print( d2)

        myDict1 = json.dumps(myDict, skipkeys=" ")

        existing_field1 = json.dumps(existing_fields)
        a="["
        if a in existing_field1 :
            existing_field1 = existing_field1[:-1]
            existing_field1 = existing_field1[-1:]
        print(existing_field1)
        #dictnew = "[" + existing_field1 + "," + myDict1 + "]"

        #DT1.extra_fields = json.loads(dictnew)

        print("dictnew")
        print(dictnew)
        #print(DT1)
        DT1.save()

    return render(request, 'communities/test.html',
                  {'DT': DT1, 'Allfields': myDict})

def addTag(request):
    r_json = {}
    if request.POST:
        API_ENDPOINT = "https://www.wikidata.org/w/api.php"
        query = request.POST['tags2']
        query.replace(" ", "&")


        params = {
            'action': 'wbsearchentities',
            'format': 'json',
            'language': 'en',
            'limit': '20',
            'search': query
        }
        wiki_request = requests.get(API_ENDPOINT, params=params)
        r_json = wiki_request.json()['search']
        r_json = json.dumps(r_json)
        r_json = json.loads(r_json)
        print(r_json)
    return render(request, 'communities/addTag.html', {'r_json': r_json})


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


def is_valid_queryparam(param):
    return param != '' and param is not None

def asearch(request):
    community = Community.objects.all()
    post = Post2.objects.all()
    qs = DataTypeObject.objects.all()
    tags = DataTypeObject.objects.all()
    print(request.GET)
    print(community)

    title_contains_query = request.GET.get('title_contains')
    community_query = request.GET.get('community_query')

    id_exact_query = request.GET.get('id_exact')
    title_or_desc_query = request.GET.get('title_or_author')
    view_count_min = request.GET.get('view_count_min')
    view_count_max = request.GET.get('view_count_max')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')


    if is_valid_queryparam(title_contains_query):
        qs = qs.filter(fields__icontains=title_contains_query)

    elif is_valid_queryparam(title_contains_query):
        post = post.filter(title__icontains=title_contains_query)


    elif is_valid_queryparam(community_query):
        community = community.filter(name__icontains=community_query)


    elif is_valid_queryparam(id_exact_query):
        qs = qs.filter(fields__icontains=id_exact_query)
        wanted_id = qs.filter(id = 1000000)
        for p in qs:
            print(p.fields['fields'][-1]['value'])
            if id_exact_query in p.fields['fields'][-1]['value']:
               print(p)
               qs = DataTypeObject.objects.filter(id = p.id)
               wanted_id = qs | wanted_id
            qs = wanted_id

            print(wanted_id)


    return render(request, 'communities/asearch.html', {'datatypeobjects': qs , 'community':community, 'posts': post })


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



