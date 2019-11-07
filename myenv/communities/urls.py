from django.urls import path

from .import views
#import the same level files

urlpatterns = [
    path('',views.index,name = "index"),
    path('<int:Community_id>',views.detail,name = "detail"),
]
