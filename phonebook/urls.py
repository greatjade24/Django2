from django.urls import path, re_path
from . import views

app_name = "PB"

urlpatterns = [
    path('index/', views.index, name="I"),
    path('add/', views.add, name="A"),
    re_path(r'^delete/(\d+)/$', views.delete, name="L"),
    re_path(r'^detail/(\d+)/$', views.detail, name='D'),
    re_path(r'^update/(\d+)/$', views.update, name="U"),
]