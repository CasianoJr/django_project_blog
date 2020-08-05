from django.shortcuts import render
from post.views import PostHomeView
from django.contrib.auth.mixins import LoginRequiredMixin
from post.models import Post


class ProfileView(LoginRequiredMixin, PostHomeView):
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user.profile).select_related('author', 'author__user')
