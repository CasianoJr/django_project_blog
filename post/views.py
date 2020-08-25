from django.shortcuts import render, get_object_or_404, reverse, redirect, HttpResponse, Http404
from .models import Post, Image, Comment
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import PostCreateForm, CommentForm, ChildCommentForm, PostImageFormSet
from django.http import HttpResponseBadRequest
from django.db.models import Q
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
        
    @method_decorator(login_required)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = PostImageFormSet(instance=self.get_object())
        return context

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

    def form_valid(self, form):
        formset = PostImageFormSet(self.request.POST, self.request.FILES, instance=self.get_object())
        if formset.is_valid():
            formset.save()
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post-home')

    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.author:
            return True
        return False

# @csrf_exempt
def search_post(request):
    queryset = Post.objects.all()
    latest_post = queryset.order_by('-date_updated')
    query = request.GET.get('search')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    else:
        queryset = None
    context = {
        'posts': queryset,
        'search_history' : query,
        'latest_post': latest_post
    }
    return render(request, 'post/search_post.html', context)

def childcomment_create(request,  comment_slug, post_slug):
    comment = get_object_or_404(Comment, slug=comment_slug)
    post = get_object_or_404(Post, slug=post_slug)
    form = ChildCommentForm(request.POST or None)
    if request.is_ajax():
        context = {'form': form, 
            'comment':comment,
            'post': post,
            }
        return render(request, 'post/child_comment_form.html', context)
    
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = request.user.profile
            form.instance.parent = comment
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'slug': post_slug}))
    else:
        return HttpResponseBadRequest('Bad Request')

    