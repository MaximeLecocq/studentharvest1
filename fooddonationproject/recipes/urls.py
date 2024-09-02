from django.urls import path
from . import views

urlpatterns = [
    path('suggestions/', views.recipe_suggestions, name='recipe_suggestions'),
]
