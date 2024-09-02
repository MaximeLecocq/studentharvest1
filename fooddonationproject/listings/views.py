from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .forms import ListingForm, SearchForm
from .models import Listing
import requests
from recipes.utils import get_ingredients_from_listing
from recipes.views import get_recipe_suggestions

#view function for rendering the homepage with filtered and paginated listings based on user queries
def homepage(request):
    title_query = request.GET.get('title', '')
    city_query = request.GET.get('city', '')
    selected_categories = request.GET.getlist('categories')

    #start with the base queryset
    listings = Listing.objects.all().order_by('-created_at')  #sort by newest listings first

    #apply title search
    if title_query:
        listings = listings.filter(title__icontains=title_query)

    #apply city search
    if city_query:
        listings = listings.filter(city__icontains=city_query)

    #apply category search with OR condition
    if selected_categories:
        queries = Q()
        for category in selected_categories:
            queries |= Q(categories__icontains=category)
        listings = listings.filter(queries)

    #pagination
    paginator = Paginator(listings, 9)  #show 9 listings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for listing in page_obj:
        listing.categories_list = listing.categories.split(',')

    #render the page with the filtered listings
    return render(request, 'homepage.html', {
        'page_obj': page_obj,
        'search_form': SearchForm(request.GET),
        'selected_categories': selected_categories
    })


#view for creating a new listing, restricted to users with a donor role
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
            listing.categories = ','.join(form.cleaned_data['categories'])
            if 'image1' not in request.FILES:
                messages.error(request, 'At least one image is required.')
                return render(request, 'listings/create_listing.html', {'form': form})
            categories = form.cleaned_data['categories']
            if 'canned' in categories:
                listing.expiry_date_canned = form.cleaned_data['expiry_date_canned']
            if 'dry' in categories:
                listing.expiry_date_dry = form.cleaned_data['expiry_date_dry']
            if 'beverages' in categories:
                listing.expiry_date_beverages = form.cleaned_data['expiry_date_beverages']
            listing.save()
            messages.success(request, 'Listing created successfully.')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm()
    return render(request, 'listings/create_listing.html', {'form': form})

#this view displays the details of a specific listing
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    categories_list = listing.categories.split(',')
    is_owner = request.user == listing.donor
    ingredients = ','.join(get_ingredients_from_listing(listing))
    recipes = get_recipe_suggestions(ingredients)
    context = {
        'listing': listing,
        'categories_list': categories_list,
        'is_owner': is_owner,
        'recipes': recipes,
    }
    return render(request, 'listings/listing_detail.html', context)


#this view displays a list of all listings created by a specific donor
def donor_listings(request, donor_id):
    donor = get_object_or_404(User, pk=donor_id)
    listings = Listing.objects.filter(donor=donor).order_by('-created_at')

    #pagination
    paginator = Paginator(listings, 9)  #show 9 listings per page
    page = request.GET.get('page')

    try:
        listings_page = paginator.page(page)
    except PageNotAnInteger:
        #if page is not an integer, deliver first page.
        listings_page = paginator.page(1)
    except EmptyPage:
        #if page is out of range, deliver last page of results.
        listings_page = paginator.page(paginator.num_pages)

    return render(request, 'listings/donor_listings.html', {
        'donor': donor,
        'listings': listings_page  #use the paginated listings
    })


#this view handles the editing of a listing; ensures that only the donor of the listing can edit it
@login_required
def edit_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.user != listing.donor:
        messages.error(request, "You are not allowed to edit this listing.")
        return redirect('listing_detail', pk=pk)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():

            if not listing.image1 and 'image1' not in request.FILES:
                messages.error(request, 'At least one image is required.')
                return render(request, 'listings/edit_listing.html', {'form': form})
                
            form.save()
            messages.success(request, 'Listing updated successfully.')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm(instance=listing)

    return render(request, 'listings/edit_listing.html', {'form': form})

#this view handles the deletion of a listing; ensures that only the donor of the listing can delete it
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

#this view handles adding a listing to a user's favorites;
#ensures the listing is only added if it is not already in the user's favorites
@login_required
def add_to_favorites(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.user in listing.favorites.all():
        messages.info(request, "This listing is already in your favorites.")
    else:
        listing.favorites.add(request.user)
        messages.success(request, "Added to your favorites!")
    return redirect(request.META.get('HTTP_REFERER', 'homepage'))


#view handles removing a listing from a user's favorites;
#ensures the listing is only removed if it is currently in the user's favorites
@login_required
def remove_from_favorites(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.user in listing.favorites.all():
        listing.favorites.remove(request.user)
        messages.success(request, "Removed from your favorites.")
    else:
        messages.info(request, "This listing is not in your favorites.")
    return redirect(request.META.get('HTTP_REFERER', 'homepage'))

#view displays a paginated list of a user's favorite listings; ensures proper pagination for better user experience
@login_required
def user_favorites(request):
    favorites = request.user.favorite_listings.all()
    paginator = Paginator(favorites, 9)  #show 9 favorite listings per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'listings/user_favorites.html', {'page_obj': page_obj})