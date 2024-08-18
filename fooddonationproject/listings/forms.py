# listings/forms.py

from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    CATEGORIES = (
        ('canned', 'Canned Goods'),
        ('dry', 'Dry Staples'),
        ('beverages', 'Beverages'),
        ('vegetables', 'Fresh Vegetables'),
        ('fruits', 'Fruits'),
    )
    
    categories = forms.MultipleChoiceField(  # Allow multiple choices
        choices=CATEGORIES,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Listing
        fields = ['title', 'description', 'address', 'categories', 'expiry_date', 'image']
