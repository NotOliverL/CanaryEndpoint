from django.contrib import admin
from .models import Endpoint, APICall

admin.site.register(Endpoint)
admin.site.register(APICall)
