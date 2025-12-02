from django.contrib import admin
from .models import CarpetType, Order, VisitorCount, Review

# Register your models here.

admin.site.register(CarpetType)
admin.site.register(Order)
admin.site.register(VisitorCount)
admin.site.register(Review)