from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.TextField()
    body = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='blog/', blank=True, null=True)
    published_at = models.DateField()
    read_minutes = models.PositiveIntegerField(default=5)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )
    message = models.TextField()
    approved = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} ({self.rating}★)"
