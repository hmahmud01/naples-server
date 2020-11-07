from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Document(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=128, null=True, blank=True)
    doctype = models.CharField(max_length=128, null=True, blank=True)
    author = models.CharField(max_length=128, null=True, blank=True)
    status = models.CharField(max_length=22, null=True, blank=True)
    document = models.FileField('document_files', upload_to='documents', blank=True, null=True)
    thumbnail = models.FileField('document_thumb', upload_to='thumbnails', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title

class TopStory(models.Model):
    document = models.ForeignKey(Document, related_name='top_document', on_delete=models.CASCADE)

    def __str__(self):
        return self.document

class Subscription(models.Model):
    first_name = models.CharField(max_length=24, null=True, blank=True)
    last_name = models.CharField(max_length=24, null=True, blank=True)
    phone = models.CharField(max_length=21, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    subscription_type = models.CharField(max_length=24, null=True, blank=True)
    charge = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.subscription_type

class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(max_length=128, null=True, blank=True)
    username = models.CharField(max_length=32, null=True, blank=True)
    phone = models.CharField(max_length=22, null=True, blank=True)
    address = models.CharField(max_length=64, null=True, blank=True)
    status = models.CharField(max_length=64, null=True, blank=True)
    subscription_type = models.CharField(max_length=64, null=True, blank=True)
    subscription = models.ForeignKey(Subscription, related_name='subscription_charge', null=True, blank=True, on_delete=models.CASCADE)
    charge = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.username

class Faq(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title