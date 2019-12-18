from django.urls import path

from .import views
from .views import post_new, post_edit, post_detail, post_list, specificpost , jsonform, newcommunity
from django.urls import include

from .views import TestDashboardView


#import the same level files

urlpatterns = [
    path('',views.index,name = "index"),
    path('allposts/<int:communityId>', views.specificpost, name='specificpost'),
    path('post/new/<int:communityId>', post_new, name='post_new'),
    path('onepost/<int:id>', views.onepost, name='onepost'),
    path('jsonform/', views.jsonform, name='jsonform'),
    path('newcommunity/', newcommunity, name='newcommunity'),
    path('search/?search=<searchtext>', views.search , name='search'),

    path('home', views.home, name='home'),
    path('api/post/', include('communities.api.urls')),


    path('datatype/new/<int:communityId>', views.data_type_creation, name='newdatatype'),

    path('field/new/<int:communityId>/<int:datatypeId>', views.field_creation, name='test'),

    path('post/<int:id>/edit/', views.post_edit, name='post_edit'),
    path('datatypelist/<int:id>', views.datatype_list, name='datatype_list'),

    #TODO:iptal postform
    #path('postform/new/<int:communityId>/<int:datatypeId>',views.post_form_creation,name='postformcreation'),

    path('datatypefields/<int:datatypeId>', views.datatypefields, name='datatypefields'),
    path('addTag/', views.addTag, name='addTag'),
    path('search/', views.asearch, name='asearch'),

    path('<int:Community_id>',views.detail,name = "detail"),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/list', post_list, name='post_list'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),



]
