from django.urls import path
from . import views

# 해당앱 내부의 url패턴
urlpatterns =[
    path('', views.landing),
]