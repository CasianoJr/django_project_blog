from django.shortcuts import render, get_object_or_404
from .models import Post
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import PostCreateForm

class PostHomeView(ListView):
    # model = Post
    queryset = Post.objects.select_related('author', 'author__user')
    template_name = 'post/post_home.html'
    context_object_name = 'posts'
    ordering = ['-date_created']
    paginate_by = 5


class PostDetailView(DetailView):
    queryset = Post.objects.all()
    template_name = 'post/post_detail.html'
    context_object_name = 'post'

class PostCreateView(CreateView):
    model = Post
    fields = ('title', 'content', 'featured', 'category',)
    template_name = 'post/post_create.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     super().dispatch(*args, **kwargs)
    

# @method_decorator(login_required, name='dispatch')
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView,):
    queryset = Post.objects.all()
    form_class = PostCreateForm
    template_name = 'post/post_update.html'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.author:
            return True
        return False



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post-home')
    template_name = 'post/post_delete.html'
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.author:
            return True
        return False

class PostDummpyView(DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list']= Post.objects.all()
        context['title']= 'Title'
        return context
    
      # redefine the queryset
    def get_queryset(self):
        # self.publisher= get_object_or_404(Post, name=self.kwargs['publisher'])
        # return Post.objects.filter(publisher=self.publisher)
        pass
       # Update specific may in detail
    def get_object(self): 
        obj - super().get_object()
        obj.date_updated = timezone.now()
        obj.save
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list']= Post.objects.all()
        context['title']= 'Title'
        return context
    
