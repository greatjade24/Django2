from django.urls import path, re_path
from . import views

app_name="BD"

urlpatterns=[
    re_path(r"^page/(\d+)/$", views.index, name="I"),
    re_path(r'^(\d+)/$', views.detail, name="D"),
    re_path(r'^(\d+)/update/$', views.update, name="U"),
    re_path(r'^(\d+)/delete/$', views.delete, name="L"),
    path('add/', views.add, name="A"),
    path('updown/', views.updown),
    path('updown/upload/', views.upload),
    path('updown/download/<boardId>/<filename>', views.download, name="down"),
    path('updown/delete/<boardId>/<filename>', views.boardDel, name="del"),
]