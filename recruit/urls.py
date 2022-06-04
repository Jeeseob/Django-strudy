from django.urls import path
from . import views

# 해당앱 내부의 url패턴
urlpatterns =[
    # class-based views
    path('create_post/', views.PostCreate.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('tag/<str:slug>/', views.show_tag_posts),
    path('search/<str:search>/', views.show_search_posts),
    path('category/<str:slug>/', views.CategoryPostList.as_view()),
    path('post/<int:pk>/', views.PostDetail.as_view()),
    path('post/<int:pk>/addcomment/', views.new_comment),
    path('post/<int:pk>/create_join/', views.JoinCreate.as_view()),
    path('join/<int:pk>', views.JoinDetail.as_view()),
    path('join/list', views.JoinList.as_view()),
    path('', views.PostList.as_view()),
]