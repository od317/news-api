from django.db import models
from django.conf import settings
from django.utils import timezone

class Investigation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    
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

class InvestigationPage(models.Model):
    investigation = models.ForeignKey(
        Investigation, 
        on_delete=models.CASCADE, 
        related_name='pages'
    )
    page_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='investigation_pages/', blank=True, null=True)
    source = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.investigation.title} - Page {self.page_number}"
    
    class Meta:
        ordering = ['page_number']
        unique_together = ['investigation', 'page_number']