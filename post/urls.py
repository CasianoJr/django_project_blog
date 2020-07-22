from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostHomeView.as_view(), name='post-home'),
    path('<slug>/', views.PostDetailView.as_view(), name='post-detail'),
]
