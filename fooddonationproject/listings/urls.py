from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),  # homepage route
    path('create/', views.create_listing, name='create_listing'),
    path('<int:pk>/', views.listing_detail, name='listing_detail'),
    path('<int:pk>/edit/', views.edit_listing, name='edit_listing'),  # edit listing route
    path('donor/<int:donor_id>/', views.donor_listings, name='donor_listings'),
    path('<int:pk>/delete/', views.delete_listing, name='delete_listing'),
]
