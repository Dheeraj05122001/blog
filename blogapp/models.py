# blog/models.py
from django.db import models
from django.contrib.auth.models import User,AbstractUser
import datetime
from django.utils.timezone import timezone 
from django.core.exceptions import ValidationError  
from tinymce.models import HTMLField
import os
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class datauser(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    qualification = models.CharField(max_length=50, null=False, blank=False, default="12")
    created = models.DateTimeField(default=datetime.datetime.now())
    profile_image = models.ImageField(upload_to='images/', null=True, blank=True)


class Post(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    title = models.CharField(max_length=200)
    content = HTMLField()
    short_description = models.CharField(max_length=255, default="No short description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,default='1')
    image = models.ImageField(upload_to='images/',default='default.jpg')
    delete_image = models.BooleanField(default=False, help_text="Tick this to delete the current image")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    views_count = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # NEW
    keywords = models.TextField(default="django,blog,post", help_text="Enter at least 3 comma-separated keywords.")


    def __str__(self):
        return self.title

    def clean(self):
        """Custom model validation to ensure at least 3 keywords are given."""
        if self.keywords:
            keyword_list = [kw.strip() for kw in self.keywords.split(',') if kw.strip()]
            if len(keyword_list) < 3:
                raise ValidationError("Please enter at least 3 keywords.")
            
    def delete(self, *args, **kwargs):
        # Delete image file if it's not the default
        if self.image and self.image.name != 'default.jpg':
            image_path = self.image.path
            if os.path.isfile(image_path):
                os.remove(image_path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        old_image = None

        if self.pk:
            old_image = Post.objects.filter(pk=self.pk).values_list('image', flat=True).first()

        # Handle manual image deletion via checkbox
        if self.delete_image and old_image and old_image != 'default.jpg':
            image_path = os.path.join(settings.MEDIA_ROOT, old_image)
            if os.path.isfile(image_path):
                os.remove(image_path)
            self.image = 'default.jpg'

        # Handle image change
        elif old_image and self.image and old_image != self.image.name and old_image != 'default.jpg':
            old_image_path = os.path.join(settings.MEDIA_ROOT, old_image)
            if os.path.isfile(old_image_path):
                os.remove(old_image_path)

        super().save(*args, **kwargs)
    
class FeaturedBlog0(models.Model):
    blog = models.OneToOneField(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Featured: {self.blog.title}"
    
class FeaturedBlog1(models.Model):
    blog = models.OneToOneField(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Featured: {self.blog.title}"
    
class FeaturedBlog2(models.Model):
    blog = models.OneToOneField(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Featured: {self.blog.title}"
    
class FeaturedBlog3(models.Model):
    blog = models.OneToOneField(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Featured: {self.blog.title}"
    
class FeaturedBlog4(models.Model):
    blog = models.OneToOneField(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Featured: {self.blog.title}"
    
class FeaturedBlog5(models.Model):
    blog = models.OneToOneField(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Featured: {self.blog.title}"



class Question(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    views_count = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # NEW
    short_description = models.CharField(max_length=160,default="No short description")
    keywords = models.TextField(default="django,question,answer", help_text="Enter at least 3 comma-separated keywords.")
    
    def __str__(self):
        return self.title
    
    def clean(self):
        """Custom model validation to ensure at least 3 keywords are given."""
        if self.keywords:
            keyword_list = [kw.strip() for kw in self.keywords.split(',') if kw.strip()]
            if len(keyword_list) < 3:
                raise ValidationError("Please enter at least 3 keywords.")
    
    
class Answer(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # NEW


    def __str__(self):
        return f"Answer by {self.author} to '{self.question.title}'"
    

class EmailOTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.otp}"
