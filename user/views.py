from django.shortcuts import render, get_object_or_404, reverse, redirect
from post.views import PostHomeView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView
from post.models import Post
from django.contrib.auth.models import User
from .models import Bio, Profile
from .forms import ProfileForm, BioFormSet
from django.contrib import messages


class ProfileView(LoginRequiredMixin, PostHomeView):
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user.profile).select_related('author', 'author__user')


class SpecificProfileView(PostHomeView):
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.filter(author=user.profile).select_related('author', 'author__user')
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bio'] = Bio.objects.filter(user__user__username=self.kwargs['username'])
        context['profile'] = get_object_or_404(Profile, user__username=self.kwargs['username'])
        return context


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView,):
    model = Profile
    form_class = ProfileForm
    template_name = 'user/update_profile.html'

    def test_func(self):
        profile = self.get_object()
        if self.request.user == profile.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = BioFormSet(instance=self.get_object())
        return context

    def form_valid(self, form):
        formset = BioFormSet(self.request.POST, self.request.FILES, instance=self.get_object())
        if formset.is_valid():
            formset.save()
        return super().form_valid(form)
