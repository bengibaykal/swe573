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
    #URL = "http://127.0.0.1:8000/api/post/list"
    #response = requests.get(URL)
    #data = response.json()
    #data = [x for x in data if x['communityId'] == communityId]
    #print(data)
    dto = DataTypeObject.objects.filter( community = community )
    print(dto)

    return render(request, 'communities/specificpost.html', { 'communityId': communityId , 'community': community , 'dto' : dto })

#TODO: sil
def onepost(request, id):
    #URL = "http://127.0.0.1:8000/api/post/list"
    #response = requests.get(URL)
    #data = response.json()
    #data = [x for x in data if x['id'] == id]
    #print(data)
    return render(request, 'communities/onepost.html', {'id':id})


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
        print(request.POST)

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

#TODO: normal search yap
def search(request, searchtext):

        #URL = "http://127.0.0.1:8000/api/post/community?search={}".format(searchtext)
        #response = requests.get(URL)
        #data = response.json()

        #print(data)
        return render(request, 'communities/onepost.html', )


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

    # if request.method == "POST":
    #     form = DataTypeForm(request.POST)
    #     if form.is_valid():
    #         post = form.save(commit=False)
    #         post.communityId = Community.objects.get(id = communityId)
    #         post.save()
    #         print(post)
    #         return redirect('index')
    # else:
    #     form = DataTypeForm()
    # return render(request, 'communities/newdatatype.html', {'form': form, 'communityId': communityId})
    community = Community.objects.get(id=communityId)
    DataType1 = DataType()

    if (request.method == "POST"):

        query = request.POST
        _mutable = query._mutable
        query._mutable = True
        del query['csrfmiddlewaretoken']
        query._mutable = False

        print(query['datatypename'])


        DataType1.community = Community.objects.get(id=communityId)
        DataType1.name = query['datatypename']
        DataType1.extra_fields = {}
        DataType1.save()
        print(DataType1.extra_fields)

    return render(request, 'communities/newdatatype.html', {'DataType': DataType1 , 'dto': DataType1 ,  'communityId': communityId , 'community': community } )

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
    #DataType.objects.all()
    Field1 = Field.objects.filter(data_type=datatypeId)


    DataTypeObject1 = DataTypeObject()
    DataTypeObject1.community = community
    DataTypeObject1.data_type = datatype


    #print(DataTypeObject1)
    if (request.method == "POST"):
        myDict = {}
        #geolocation = request.POST.get('geolocation')
        #name = request.POST.get('name')
        #if geolocation != "":
        #    myDict = {'name': "geolocation",
        #              'value': request.POST['geolocation'],
        #              }
        #elif geolocation == "":
        #    print("Girmedi")
        #elif name != "":
        #    myDict = {'name': "name",
        #              'value': request.POST['name'],
        #              }
        #else:
        #    print("hiç girmedi")
        #
        #print(myDict)

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
          myDict= {  'name':  key,
                   'value' :   request.POST[key]
                  }

          f['fields'].append(myDict)

        tagname = request.POST['tags']
        print(tagname)
        tagname = tagname.split(',')
        print(tagname)

        #TODO:tagler ayrı yazılacaksa searchte de burada aranmalı
        #tags= {}
        #tags['tags'] = []
        #for tagpair in tagname:
        #  if ':' in tagpair:
        #    m = tagpair.index(':')
        #    l = tagpair[:m]
        #    q = tagpair[m:]
        #    print(l)
        #    print(q)
        #
        #    tags1 = { 'tagname' :  l,
        #            'Qvalue'   : q
        #              }
        #    tags['tags'].append(tags1)
        #f['fields'].append(tags)
        #print(f)

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

            return redirect('index')
    else:
        form = FieldForm()
    return render(request, 'communities/test.html',
                  {'form': form, 'communityId': communityId, 'datatypeId': datatypeId})

#TODO:Not using field creation2
def field_creation2(request, communityId, datatypeId):
    myDict = {}
    Community1 = Community.objects.get(id=communityId)
    DT1 = DataType.objects.get(id=datatypeId)

    if (request.method == "POST"):
        query = request.POST
        _mutable = query._mutable
        query._mutable = True
        del query['csrfmiddlewaretoken']
        query._mutable = False

        print(query)
        queryDict = query.keys()

#######################################
        f = {}
        f['extra_fields'] = []
        for key in queryDict:
          myDict= {  key, request.POST[key] }
          print(myDict)

          f['fields'].append(myDict)
        #DataTypeObject1.fields = f
        #DataTypeObject1.save()
        #print(DataTypeObject1)

        print(queryDict2)
        myDict = {}
        for key in queryDict:
            myDict[key] = request.POST[key]
        myDict['community'] = communityId
        myDict['data_type'] = datatypeId
        print(myDict)

        #DT1.save()

    return render(request, 'communities/test.html',  {'DT': DT1, 'Allfields': myDict})

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

#TODO: Delete
def post_form_creation(request, communityId, datatypeId):
    #form = PostTypeForm(request.POST)
    #post = form
    #post.modified_by = request.user
    #post.communityId = Community.objects.get(id=communityId)
    #print(post)
    #community = Community.objects.get(id=communityId)
    #datatype = DataType.objects.get(id=datatypeId)
    #extrafields = datatype.extra_fields
    #name = extrafields['name']
    #print(name)
    return render(request, 'communities/postformcreation.html', { })

# search helper function
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
    field_query = request.GET.get('field_query')
    all_fields = request.GET.get('all_fields')

    title_or_desc_query = request.GET.get('title_or_author')
    view_count_min = request.GET.get('view_count_min')
    view_count_max = request.GET.get('view_count_max')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    print (all_fields)

    ## advanced combined search
    if all_fields == 'on':
        # Filter post titles
        #qs = qs.filter(fields__icontains=title_contains_query)
        wanted_id = qs.filter(id=1000000)
        print("title search")
        qs = qs.filter(fields__icontains=title_contains_query)
        for obj in qs:
            # print(obj)
            for a in obj.fields['fields']:
                # print( a)
                if a['name'] == 'title':
                    # print("its title")
                    # print(a['value'])
                    if title_contains_query in a['value']:
                        print(a['value'])
                        dto = DataTypeObject.objects.filter(id=obj.id)
                        wanted_id = dto | wanted_id
                        print("wanted")
                        print(wanted_id)
        qs = wanted_id
        print(qs)
        ### title filtered.

        # Filter communities of the posts
        qs2 = qs.filter(community__name__icontains=community_query)
        print("community filter")
        print(qs2)
        wanted_id = qs2.filter(id=1000000)
        #Post communities filtered.

        #Filter tags
        for p in qs2:
            #print(p.fields['fields'][-1]['value'])
            if id_exact_query in p.fields['fields'][-1]['value']:
                print(p)
                qs3 = DataTypeObject.objects.filter(id=p.id)
                wanted_id = qs3 | wanted_id
        qs = wanted_id
        print(qs)
        #tags filtered.

        #filter fields
        Fields = Field.objects.filter(name__icontains=field_query)
        wanted_id = DataTypeObject.objects.filter(id=1000000)
        for field in Fields:
            print(field.data_type)
            dt = DataType.objects.filter(name__icontains = field.data_type)

            for a in dt:
                dto = qs.filter(data_type = a.id)
                wanted_id = dto | wanted_id
        print(wanted_id)
        qs = wanted_id
        print(qs)
        #fields filtered

        ## community filter
        community = community.filter(name__icontains=community_query)

    ## JSONFILTER! filter in jsonField field in DataTypeObject which has the matching TITLE
    elif is_valid_queryparam(title_contains_query):
        #to be able to create empty qs ? find a better way!
        wanted_id = qs.filter(id=1000000)
        print("title search")
        qs = qs.filter(fields__icontains=title_contains_query)
        for obj in qs:
            #print(obj)
            for a in obj.fields['fields']:
                #print( a)
                if a['name'] == 'title':
                    #print("its title")
                    #print(a['value'])
                    if title_contains_query in a['value']:
                        print(a['value'])
                        dto = DataTypeObject.objects.filter(id=obj.id)
                        wanted_id = dto | wanted_id
                        print("wanted")
                        print(wanted_id)
        qs = wanted_id
        print(qs)

    #elif is_valid_queryparam(title_contains_query):
        #post = post.filter(title__icontains=title_contains_query)


    elif is_valid_queryparam(community_query):
        qs = qs.filter(community__id__icontains=community_query)
        print(qs)
        community = community.filter(name__icontains=community_query)
        wanted_id = qs.filter(id=1000000)
        print(community)

    #collect all objects that contains search query in their texts
    elif is_valid_queryparam(id_exact_query):
        qs = qs.filter(fields__icontains=id_exact_query)
        wanted_id = qs.filter(id = 1000000)
        for p in qs:
            #print(p.fields['fields'][-1]['value'])
            if id_exact_query in p.fields['fields'][-1]['value']:
               print(p)
               qs = DataTypeObject.objects.filter(id = p.id)
               wanted_id = qs | wanted_id
            qs = wanted_id

            print(wanted_id)

    elif is_valid_queryparam(field_query):
        qs = Field.objects.filter(name__icontains=field_query)



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



