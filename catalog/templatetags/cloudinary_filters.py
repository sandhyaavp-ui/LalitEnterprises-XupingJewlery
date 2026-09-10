from django import template

register = template.Library()


@register.filter
def cloudinary_optimize(url):
    """Inserts f_auto (best format per browser) and q_auto (auto quality)
    right after '/upload/' in a Cloudinary URL, cutting image payload with
    no visible quality loss."""
    if url and '/upload/' in url:
        return url.replace('/upload/', '/upload/f_auto,q_auto/', 1)
    return url
