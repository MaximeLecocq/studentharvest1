from django.contrib import admin
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'donor', 'created_at', 'expiry_date')
    search_fields = ('title', 'description')
    list_filter = ('categories', 'expiry_date')
