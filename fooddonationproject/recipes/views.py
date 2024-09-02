from django.shortcuts import render
import requests
from .utils import get_ingredients_from_listing

#function fetches recipe suggestions from the Spoonacular API based on provided ingredients
def get_recipe_suggestions(ingredients):
    api_key = 'edae9cc8988d4cf18a9f7adf2642416a'
    #makes a GET request to the API to find recipes based on the provided ingredients
    response = requests.get(
        f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=5&apiKey={api_key}'
    )
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        #handle API errors or lack of data
        return []



#recipe_suggestions view that dynamically come from a form
def recipe_suggestions(request):
    #get ingredients from the query parameters if provided, otherwise default to an empty string
    ingredients = request.GET.get('ingredients', '')
    
    if ingredients:
        #call the recipe suggestion function with the user-provided ingredients
        recipes = get_recipe_suggestions(ingredients)
    else:
        #if no ingredients provided, display an empty list or a message
        recipes = []

    return render(request, 'recipes/recipe_suggestions.html', {'recipes': recipes, 'ingredients': ingredients})
