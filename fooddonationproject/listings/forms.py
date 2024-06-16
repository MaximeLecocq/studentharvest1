from django import forms
from django.forms import inlineformset_factory
from .models import Listing, ListingImage

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description']

ListingImageFormSet = inlineformset_factory(
    Listing,
    ListingImage,
    fields=['image'],
    extra=3,  # Allow up to 3 images
    can_delete=True
)
