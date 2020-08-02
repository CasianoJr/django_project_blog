from django.shortcuts import render, get_object_or_404, reverse, redirect, HttpResponse, Http404
from .models import Post, Image, Comment
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import PostCreateForm, CommentForm
from django.http import HttpResponseBadRequest
# from django.views.decorators.csrf import csrf_exempt


class PostHomeView(ListView):
    queryset = Post.objects.select_related('author', 'author__user')
    template_name = 'post/post_home.html'
    context_object_name = 'posts'
    ordering = ['-date_created']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostCreateForm
        return context

    def get(self, request, *args, **kwargs):
        # if request.is_ajax():
        #     return render(request, 'post/post_create.html', {'form': PostCreateForm})
        # else:
        return super().get(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = PostCreateForm(request.POST)
        if form.is_valid():
            form.instance.author = self.request.user.profile
            form.save()
            images = request.FILES.getlist('images')
            for image in images:
                img = Image(thumbnail=image, post=form.instance)
                img.save()
            return redirect(reverse("post-detail", kwargs={
                'slug': form.instance.slug}))


# @csrf_exempt
def post_like_view(request, slug):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest('Not authenticated')
    if request.is_ajax():
        post = get_object_or_404(Post, slug=slug)
        if request.user in post.like.all():
            post.like.remove(request.user)
        else:
            post.like.add(request.user)
        return render(request, 'post/footer_post_buttons.html', {"post": post})
    else:
        return HttpResponseBadRequest('Bad Request')


class PostDetailView(DetailView):
    queryset = Post.objects.all()
    template_name = 'post/post_detail.html'
    context_object_name = 'post'

    def get_template_names(self):
        if self.request.is_ajax():
            return super().get_template_names()
        else:
            return 'post/post_detail_w_base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST or None)
        if form.is_valid():
            form.instance.author = request.user.profile
            form.instance.post = post
            form.save()
        return self.get(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # fields = ('title', 'content', 'featured', 'category',)
    # template_name = 'post/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest('Bad Request')

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     super().dispatch(*args, **kwargs)


# @method_decorator(login_required, name='dispatch')
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView,):
    queryset = Post.objects.all()
    form_class = PostCreateForm
    template_name = 'post/post_update.html'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest('Bad Request')

    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post-home')

    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.author:
            return True
        return False

# class PostDummpyView(DetailView):
#         pass
      # redefine the queryset
    # def get_queryset(self)
        # self.publisher= get_object_or_404(Post, name=self.kwargs['publisher'])
        # return Post.objects.filter(publisher=self.publisher)
       # Update specific may in detail
    # def get_object(self):
        # obj - super().get_object()
        # obj.date_updated = timezone.now()
        # obj.save
        # return obj
