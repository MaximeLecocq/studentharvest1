from django.shortcuts import render, redirect, get_object_or_404
from .models import Listing, ListingImage
from .forms import ListingForm, ListingImageFormSet
from django.contrib.auth.decorators import login_required


@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        formset = ListingImageFormSet(request.POST, request.FILES, queryset=ListingImage.objects.none())

        if form.is_valid() and formset.is_valid():
            listing = form.save(commit=False)
            listing.donor = request.user
            listing.save()

            for form in formset:
                if form.cleaned_data.get('image'):
                    photo = form.save(commit=False)
                    photo.listing = listing
                    photo.save()

            return redirect('listing_detail', pk=listing.pk)  # Redirect to listing detail page

    else:
        form = ListingForm()
        formset = ListingImageFormSet(queryset=ListingImage.objects.none())

    return render(request, 'listings/create_listing.html', {'form': form, 'formset': formset})


# def create_listing(request):
#     if request.method == 'POST':
#         form = ListingForm(request.POST)
#         formset = ListingImageFormSet(request.POST, request.FILES)
#         if form.is_valid() and formset.is_valid():
#             listing = form.save(commit=False)
#             listing.donor = request.user
#             listing.save()
#             for form in formset:
#                 if form.cleaned_data.get('image'):
#                     photo = form.save(commit=False)
#                     photo.listing = listing
#                     photo.save()
#             return redirect('listing_list')
#     else:
#         form = ListingForm()
#         formset = ListingImageFormSet()
#     return render(request, 'listings/create_listing.html', {'form': form, 'formset': formset})

def listing_list(request):
    listings = Listing.objects.all().order_by('-created_at')
    return render(request, 'listings/listing_list.html', {'listings': listings})



def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'listings/listing_detail.html', {'listing': listing})
