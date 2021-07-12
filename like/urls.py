from django.urls import path, re_path

from . import views

urlpatterns = [
    path('up_down/', views.up_down, name='up_down'),
]
