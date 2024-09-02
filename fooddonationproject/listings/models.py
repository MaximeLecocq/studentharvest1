from django.db import models
from users.models import User
from django.conf import settings

#this code defines the Listing model, which represents a food listing in the app.
#each listing includes fields such as title, description, donor, address, categories, expiry dates, images, and favorites.
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
    donor = models.ForeignKey('users.User', on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.CharField(max_length=255)
    expiry_date_canned = models.DateField(blank=True, null=True)
    expiry_date_dry = models.DateField(blank=True, null=True)
    expiry_date_beverages = models.DateField(blank=True, null=True)
    image1 = models.ImageField(upload_to='images/listings/', blank=False)
    image2 = models.ImageField(upload_to='images/listings/', blank=True, null=True)
    image3 = models.ImageField(upload_to='images/listings/', blank=True, null=True)
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorite_listings', blank=True)

    def __str__(self):
        return self.title

