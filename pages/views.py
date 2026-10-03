import os
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Collection
from .forms import TestimonialForm
from .models import BlogPost, Testimonial

LLM_FILES_DIR = os.path.join(os.path.dirname(__file__), 'llm_files')


def home(request):
    collections = Collection.objects.all()
    return render(request, 'pages/home.html', {'collections': collections})


def about(request):
    collections = Collection.objects.all()
    testimonials = Testimonial.objects.filter(approved=True)
    testimonials_data = [
        {
            'name': t.name,
            'designation': 'Verified Reseller',
            'quote': t.message,
            'rating': t.rating,
        }
        for t in testimonials
    ]
    review_form = TestimonialForm()
    return render(request, 'pages/about.html', {
        'collections': collections,
        'testimonials': testimonials,
        'testimonials_data': testimonials_data,
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
            messages.success(request, "Thanks for sharing your experience — your review will appear once it's checked.", extra_tags="review_submitted")
            return redirect('pages:about')
    else:
        form = TestimonialForm()
    return render(request, 'pages/submit_review.html', {'form': form})


def robots_txt(request):
    content = """# AI search / answer-engine crawlers — allowed to retrieve pages for citation
User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

# AI training crawlers — not allowed to use this content for model training
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: Googlebot
Disallow: /admin/
Disallow: /admin/dashboard/
Allow: /

User-agent: *
Disallow: /admin/
Disallow: /admin/dashboard/
Allow: /

Sitemap: https://lalitenterprise.in/sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain; charset=utf-8')


def _serve_llm_file(filename):
    with open(os.path.join(LLM_FILES_DIR, filename), encoding='utf-8') as f:
        return HttpResponse(f.read(), content_type='text/markdown; charset=utf-8')


def llms_txt(request):
    return _serve_llm_file('llms.txt')


def llms_full_txt(request):
    return _serve_llm_file('llms-full.txt')
