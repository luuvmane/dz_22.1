from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    views = models.IntegerField(default=0)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Version(models.Model):
    product = models.ForeignKey(Product, related_name='versions', on_delete=models.CASCADE)
    version_number = models.CharField(max_length=50)
    version_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    release_date = models.DateField(default=timezone.now)
    description = models.TextField(default='Описание по умолчанию')

    def __str__(self):
        return f"{self.version_number} - {self.version_name}"


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    preview_image = models.ImageField(upload_to='blog_previews/')
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blogpost_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
