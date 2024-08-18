# listings/models.py

from django.db import models
from users.models import User

class Listing(models.Model):
    CATEGORY_CHOICES = (
        ('canned', 'Canned Goods'),
        ('dry', 'Dry Staples'),
        ('beverages', 'Beverages'),
        ('vegetables', 'Fresh Vegetables'),
        ('fruits', 'Fruits'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.CharField(max_length=255)  # We will save the selected categories as a comma-separated string
    expiry_date = models.DateField()
    image = models.ImageField(upload_to='images/listings/', blank=True, null=True)

    def __str__(self):
        return self.title
