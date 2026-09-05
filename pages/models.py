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
