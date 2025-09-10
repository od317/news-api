from django.db import models
from django.conf import settings
from django.utils import timezone

class Resource(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class News(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()  # Large amount of text
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    resources = models.ManyToManyField(Resource, blank=True, related_name='news_articles')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='news_articles'
    )
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        elif not self.is_published and self.published_at:
            self.published_at = None
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name_plural = 'News'