from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostHomeView.as_view(), name='post-home'),
    path('create/', views.PostCreateView.as_view(), name='post-create'),
    path('search/', views.search_post, name='post-search'),
    path('<slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('<slug>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('<slug>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('<slug>/like/', views.post_like_view, name='post-like'),
    path('<post_slug>/<comment_slug>/childcomment/', views.childcomment_create, name='post-create_child'),
]
