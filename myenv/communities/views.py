from django.shortcuts import render,get_object_or_404

from django.http import HttpResponse

from .models import Community

# Create your views here.

def index(request):
    communities = Community.objects
    return render(request,'communities/index.html',{'communities': communities})

def detail(request, Community_id):
    Community_detail = get_object_or_404(Community, pk=Community_id)
    return render(request, 'communities/detail.html', {'community': Community_detail})
