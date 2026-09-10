from django import template

register = template.Library()


@register.filter
def cloudinary_optimize(url, width=None):
    """Inserts f_auto (best format per browser) and q_auto (auto quality)
    right after '/upload/' in a Cloudinary URL, cutting image payload with
    no visible quality loss. Pass a `width` to also cap the served
    resolution (c_limit never upscales) — the images here are uploaded at
    full camera/WhatsApp resolution, so without this a small grid
    thumbnail still downloads the full-size original."""
    if not url or '/upload/' not in url:
        return url
    params = 'f_auto,q_auto'
    if width:
        params += f',w_{width},c_limit'
    return url.replace('/upload/', f'/upload/{params}/', 1)
