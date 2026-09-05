from django.shortcuts import render, get_object_or_404
from catalog.models import Collection
from .models import BlogPost


def home(request):
    collections = Collection.objects.all()
    return render(request, 'pages/home.html', {'collections': collections})


def blogs(request):
    posts = BlogPost.objects.all()
    return render(request, 'pages/blogs.html', {'posts': posts})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'pages/blog_detail.html', {'post': post})


def terms(request):
    return render(request, 'pages/terms.html')


def privacy(request):
    return render(request, 'pages/privacy.html')
