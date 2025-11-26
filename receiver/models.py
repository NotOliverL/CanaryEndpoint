from django.db import models

class Endpoint(models.Model):
    RESPONSE_NOT_FOUND = 'NOT_FOUND'
    RESPONSE_REDIRECT = 'REDIRECT'
    RESPONSE_IMAGE = 'IMAGE'
    RESPONSE_REFERER = 'REFERER'
    RESPONSE_CHOICES = [
        (RESPONSE_NOT_FOUND, 'Not Found'),
        (RESPONSE_REDIRECT, 'Redirect'),
        (RESPONSE_IMAGE, 'Image'),
        (RESPONSE_REFERER, 'Referer'),
    ]

    name = models.CharField(max_length=100)
    path = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    token = models.CharField(max_length=64, blank=True, null=True)
    response_type = models.CharField(max_length=20, choices=RESPONSE_CHOICES, default=RESPONSE_NOT_FOUND)
    response_redirect_url = models.CharField(max_length=1000, blank=True, null=True)
    response_image = models.ImageField(upload_to='endpoint_images/', blank=True, null=True)
    response_image_referer_success = models.ImageField(upload_to='endpoint_images/', blank=True, null=True)
    response_image_referer_failure = models.ImageField(upload_to='endpoint_images/', blank=True, null=True)
    response_referer_url = models.CharField(max_length=1000, blank=True, null=True)

class APICall(models.Model):
    endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    payload = models.JSONField()
    remote_ip = models.GenericIPAddressField(null=True, blank=True)
    method = models.CharField(max_length=10)
    headers = models.JSONField(blank=True, null=True)
    query_params = models.JSONField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    user_agent = models.CharField(max_length=256, blank=True, null=True)
    referer_status = models.BooleanField(default=True, null=True)