from datetime import date
from django.db import migrations

POSTS = [
    (
        'How to Start Your Own Jewellery Reselling Business with Minimal Investment',
        'start-jewellery-reselling-minimal-investment',
        date(2026, 3, 12),
        6,
        "Thinking of starting a jewellery reselling business but worried about upfront costs? "
        "Here's how resellers across India are building profitable businesses with small "
        "starting inventories, flexible MOQs, and smart sourcing.",
    ),
    (
        'MOQ vs MOP Explained: What Every Reseller Should Know Before Bulk Ordering',
        'moq-vs-mop-explained',
        date(2026, 3, 5),
        5,
        "Confused between MOQ and MOP? This guide breaks down exactly what these terms mean, "
        "why they matter, and how understanding them can help you place smarter wholesale orders.",
    ),
    (
        'Xuping Jewellery 101: Why Authorised Agents Matter for Quality & Trust',
        'xuping-jewellery-101-authorised-agents',
        date(2026, 2, 22),
        7,
        "Not all Xuping jewellery suppliers are the same. Learn what it means to buy from an "
        "authorised agent, and why this one decision can protect your business from counterfeit "
        "stock and quality issues.",
    ),
    (
        'How to Price Your Imitation Jewellery for Maximum Profit Margins',
        'price-imitation-jewellery-for-profit',
        date(2026, 2, 10),
        6,
        "Pricing too high can scare buyers away; pricing too low eats your profits. Here's a "
        "simple framework resellers can use to price imitation jewellery for healthy margins "
        "without losing customers.",
    ),
]


def seed_posts(apps, schema_editor):
    BlogPost = apps.get_model('pages', 'BlogPost')
    for title, slug, published_at, read_minutes, excerpt in POSTS:
        BlogPost.objects.get_or_create(
            slug=slug,
            defaults={
                'title': title,
                'published_at': published_at,
                'read_minutes': read_minutes,
                'excerpt': excerpt,
                'body': '',
            },
        )


def unseed_posts(apps, schema_editor):
    BlogPost = apps.get_model('pages', 'BlogPost')
    BlogPost.objects.filter(slug__in=[slug for _, slug, _, _, _ in POSTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_blogpost_redesign'),
    ]

    operations = [
        migrations.RunPython(seed_posts, unseed_posts),
    ]
