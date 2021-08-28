from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.list import MultipleObjectMixin
from .models import *


class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'BetaBlog'
        return context

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class PostPage(DetailView):
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class PostByCategory(ListView):
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    paginate_by = 6
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(categories__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context
