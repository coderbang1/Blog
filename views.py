from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


def homepage(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'Bblog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'Bblog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3


class UserPostListView(ListView):
    model = Post
    template_name = 'Bblog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'Bblog/about.html', )


def search(request):
    query = request.GET['query']
    posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)
                                )
    context = {
        'posts': posts
    }
    return render(request, 'bblog/search.html', context)
