from django.shortcuts import render, redirect ,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings
from .models import SearchQuery
import json

# Create your views here.
def base(request):
    return render(request , "base.html")

def about(request):   
    return render(request , "about.html")


# def home(request):
    
#     last_5_records =  SearchQuery.objects.all().order_by('-timestamp')[:5]
    
#     return render(request, "home.html", {"records": last_5_records})

# Function to fetch recipes from the API
def fetch_recipes(query):
    api_url = 'https://api.edamam.com/api/recipes/v2'
    params = {
        'type': 'public',
        'q': query,  
        'app_id': settings.EDAMAM_API_ID,
        'app_key': settings.EDAMAM_API_KEY
    }

    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        return response.json() 
    else:
        return None 



def home(request):
    if request.user.is_authenticated:
  
        last_5_records = SearchQuery.objects.filter(user=request.user).values('query').distinct().order_by('-timestamp')[:8]
        
       
        unique_recipe = set()

        
        for record in last_5_records:
            unique_recipe.add(record['query'])
        
        print(unique_recipe)

        search_results = []  


        for query in unique_recipe:
            recipes = fetch_recipes(query)  
            
            if recipes:
                
                limited_recipes = recipes.get('hits', [])[:3]
                
                
                if limited_recipes:
                    search_results.append({
                        'query': query,
                        'recipes': limited_recipes,  
                    })
    else:
        
        search_results = []

   
    return render(request, "home.html", {
        "search_results": search_results,
    })





def user_signup(request):
    if request.method =="POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.create_user(username = username , email = email , password = password )
        user.save()
        return render(request , "login.html")
    return render(request,"signup.html")


def user_login(request):
    if request.method =="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username = username , password = password)
        if user :
            login(request, user)
            return redirect("about")
    return render (request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')  




def save_data(request):
    recipes = []
    query = ''  
    
    if request.method == 'POST':
        query = request.POST.get('query')  
        data = fetch_recipes(query)  
        
       
        if query:
            SearchQuery.objects.create(query=query, user=request.user if request.user.is_authenticated else None)
            
            if data:
                recipes = data.get('hits', [])
            else:
                recipes = []
    
    return render(request, 'home.html', {
        'recipes': recipes,
        'query': query,
    })


