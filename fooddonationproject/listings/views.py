from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ListingForm
from .models import Listing
from users.models import User

def homepage(request):
    listings = Listing.objects.all().order_by('-created_at')
    return render(request, 'homepage.html', {'listings': listings})

@login_required
def create_listing(request):
    if request.user.role != 'donor':
        messages.error(request, 'Only donors can create listings.')
        return redirect('home')

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.donor = request.user
            listing.categories = ','.join(form.cleaned_data['categories'])  # Join selected categories
            listing.save()
            messages.success(request, 'Listing created successfully.')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm()

    return render(request, 'listings/create_listing.html', {'form': form})

def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    is_owner = request.user == listing.donor
    categories_list = listing.categories.split(",")  # Split the categories string into a list
    return render(request, 'listings/listing_detail.html', {
        'listing': listing,
        'is_owner': is_owner,
        'categories_list': categories_list  # Pass the categories list to the template
    })


def donor_listings(request, donor_id):
    donor = get_object_or_404(User, pk=donor_id)
    listings = Listing.objects.filter(donor=donor).order_by('-created_at')
    return render(request, 'listings/donor_listings.html', {
        'donor': donor,
        'listings': listings
    })


@login_required
def edit_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.user != listing.donor:
        messages.error(request, "You are not allowed to edit this listing.")
        return redirect('listing_detail', pk=pk)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Listing updated successfully.')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm(instance=listing)

    return render(request, 'listings/edit_listing.html', {'form': form})


@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    
    if request.method == 'POST':
        if request.user == listing.donor:
            listing.delete()
            messages.success(request, 'Listing deleted successfully.')
            return redirect('homepage')
        else:
            messages.error(request, 'You do not have permission to delete this listing.')
            return redirect('listing_detail', pk=pk)
    
    return render(request, 'listings/confirm_delete.html', {'listing': listing})