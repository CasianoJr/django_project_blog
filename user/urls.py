from django.urls import path
from .views import ProfileView, SpecificProfileView, ProfileUpdateView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='user-profile'),
    path('<username>/', SpecificProfileView.as_view(), name='users'),
    path('<pk>/update/', ProfileUpdateView.as_view(), name='user-update'),
]