from django.shortcuts import render, get_object_or_404, HttpResponse

from django.http import HttpResponse
from django.shortcuts import render
from .models import Community, Post

from .forms import PostForm, CommunityForm, CustomForm
from django.shortcuts import redirect
from django.utils import timezone
import requests
import json


from .forms import CustomForm

def index(request):
    communities = Community.objects
    return render(request,'communities/index.html', {'communities': communities})

def specificpost(request, communityId):
    #URL = "http://127.0.0.1:8000/api/post/list?search={}".format(communityId)
    URL = "http://127.0.0.1:8000/api/post/list"
    response = requests.get(URL)
    data = response.json()
    #idcom = response.json()[0]["communityId"]
    #idcom = json.dumps(idcom)
    #idcom = json.loads(idcom)
    data = [x for x in data if x['communityId'] == communityId]
    print(data)
    return render(request, 'communities/specificpost.html', {'data': data, 'communityId': communityId})

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

#def jsonform(request):
#    return render(request, 'communities/jsonform.html', {'form': CustomForm()})

def jsonform(request):

    #form = CustomForm(request.POST)
    #jsondata = form.json()
    #print(jsondata)
    return render(request, 'communities/jsonform.html', {'form': CustomForm()})

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
    return render(request, 'communities/newcommunity.html', {'form': form })

#TODO:community search
def search(request, searchtext):

        URL = "http://127.0.0.1:8000/api/post/community?search={}".format(searchtext)
        response = requests.get(URL)
        data = response.json()

        print(data)
        return render(request, 'communities/onepost.html', {'data': data, 'id': id})










########

def jsonform1(request):

    json_form = CustomForm(request.POST)
    form_class = dynaform.get_form(json_form)
    data = {}
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
    else:
        form = form_class()

    return render_to_response( "jsonform.html", {
        'form': form,  'data': data,
    }, RequestContext(request) )

def detail(request, Community_id):
    Community_detail = get_object_or_404( Community, pk=Community_id)
    post = Post.objects
    Post.objects.all()
    Communities = Community.objects
    return render(request, 'communities/detail.html',  {'community': Community_detail,'post': post, 'Communities': Communities})


def post_update(request):
    form = 'Posts Update'
    return HttpResponse(form)

def post_delete(request):
    form = 'Posts Delete'
    return HttpResponse(form)



def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'communities/post_edit.html', {'form': form})

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



