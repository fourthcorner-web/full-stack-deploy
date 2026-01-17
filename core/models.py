from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify

class Job(models.Model):
    DIVISION_CHOICES = [
        ('ENGINEERING CONSTRUCTION', 'ENGINEERING CONSTRUCTION'),
        ('ELECTRICAL & POWER SYSTEMS', 'ELECTRICAL & POWER SYSTEMS'),
        ('FIRE & INDUSTRIAL SAFETY', 'FIRE & INDUSTRIAL SAFETY'),
    ]

    title = models.CharField(max_length=200)
    division = models.CharField(max_length=100, choices=DIVISION_CHOICES)
    location = models.CharField(max_length=100, default="Basra Headquarters")
    description = models.TextField(help_text="General summary of the role")
    requirements = models.TextField(help_text="Type each requirement on a new line")
    is_active = models.BooleanField(default=True)
    posted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.division})"

    class Meta:
        ordering = ['-posted_date']


webp_val = FileExtensionValidator(allowed_extensions=['webp'])

from django.contrib.auth.models import User # Add this

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=1) # Default to first admin
    thumbnail = models.ImageField(upload_to='blog/thumbs/', validators=[webp_val])
    summary = models.TextField(max_length=500)
    # Changed from auto_now_add so you can edit it if needed
    created_at = models.DateTimeField(auto_now_add=True) 

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Check for uniqueness, excluding current instance if updating
            queryset = Post.objects.filter(slug=slug)
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            while queryset.exists():
                slug = f"{base_slug}-{counter}"
                queryset = Post.objects.filter(slug=slug)
                if self.pk:
                    queryset = queryset.exclude(pk=self.pk)
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

class PostSection(models.Model):
    post = models.ForeignKey(Post, related_name='sections', on_delete=models.CASCADE)
    heading = models.CharField(max_length=200, blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='blog/sections/', blank=True, null=True, validators=[webp_val])
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']



class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)  # e.g., FIRE & INDUSTRIAL SAFETY
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Project Categories"

    def has_more_projects(self):
        # Logic: If TOTAL projects in database > 3, show the "View All" button
        return self.projects.count() > 3
    
    def __str__(self):
        return self.name

class Project(models.Model):
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='projects/thumbs/')
    short_desc = models.CharField(max_length=255)
    
    # Popup Header Details
    status = models.CharField(max_length=100, default="Active / Completed")
    location = models.CharField(max_length=100, default="Rumaila Field (ROO)")
    
    # Checkbox logic: Use this ONLY to pick which 3 appear on the landing page
    is_featured = models.BooleanField(default=False, verbose_name="Show on Homepage")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class ProjectSection(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=200) # Section Heading in Popup
    image = models.ImageField(upload_to='projects/sections/')
    description = models.TextField() # Section Paragraph
    order = models.PositiveIntegerField(default=0) # Controls 1 to 5 sequence

    class Meta:
        ordering = ['order']