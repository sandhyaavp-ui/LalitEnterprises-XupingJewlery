from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Collection
from .forms import TestimonialForm
from .models import BlogPost, Testimonial


def home(request):
    collections = Collection.objects.all()
    return render(request, 'pages/home.html', {'collections': collections})


def about(request):
    collections = Collection.objects.all()
    testimonials = Testimonial.objects.filter(approved=True)
    review_form = TestimonialForm()
    return render(request, 'pages/about.html', {
        'collections': collections,
        'testimonials': testimonials,
        'review_form': review_form,
    })


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


def submit_review(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for sharing your experience — your review will appear once it's checked.")
            return redirect('pages:about')
    else:
        form = TestimonialForm()
    return render(request, 'pages/submit_review.html', {'form': form})


def robots_txt(request):
    content = """User-agent: *
Disallow: /admin/
Disallow: /admin/dashboard/
Allow: /

Sitemap: https://lalitenterprise.in/sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain')
