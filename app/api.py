import requests
from __init__ import *
import os

def get_key(s):
    with open(s) as f:
        k = f.readlines() #api key
    key = k[0].strip() #changes the key from a list to a string
    return key

def get_title(x):
    k = get_key("keys/key_spoonacular.txt")
    url = f"https://api.spoonacular.com/recipes/{x}/information?apiKey={k}" 
    #print(url2)
    res = requests.get(url)
    recipes_api_summary = res.json()['title']
    return recipes_api_summary

def get_photo(x):
    url = f"https://api.spoonacular.com/recipes/{x}/information?apiKey=7081bf709f0d44b7984587105086357f"
    res = requests.get(url)
    recipes_api_summary = res.json()['image']
    return recipes_api_summary

#Given a search query, return a list of foods.
def get_url(name):
    #Give me the JSON thing associated with the search results produced by name
    k = get_key('keys/key_spoonacular.txt')
    url = f"https://api.spoonacular.com/recipes/complexSearch?query={name}&apiKey={k}"
    results_list = requests.get(url).json()
    recipe_url = ""
    #Try to get the results of our search.
    try:
        recipes_api = results_list["results"]
        for i in recipes_api:
            if name == i['title']:
                api_id = i['id']

                #url to get recipe name from id
                url2 = f"https://api.spoonacular.com/recipes/{api_id}/information?apiKey={k}"
                res2 = requests.get(url2)
                recipe_url = res2.json()["spoonacularSourceUrl"]
                return recipe_url

    #You reached the API call quota.
    except KeyError:
        print("get_url(name) in api.py")
        print(results_list)
        recipe_url = results_list['message']
    return recipe_url

def search_recipe(query, l, u): #searches using query as a keyword and returns results l to u
    k = get_key('keys/key_edamam.txt')
    url =  "https://api.edamam.com/api/recipes/v2"
    res = requests.get(url, params={'type':'public', 'app_id':"904296dd", 'app_key':k, 'q': query})
    results = []
    while (l<u):
        results.append(res.json()['hits'][l]['recipe']['label']) #the index after hits is the x result (1 is second result from searching)
        l = l+1
    return results 
    
# populate list with randomly generated urls [title, image, and sourceUrl]
def makeList(i):
    recipe_titles = []
    recipe_images = []
    recipe_urls = []
    recipe_summaries = []
    #Get the spoonacular API key
    k = get_key('keys/key_spoonacular.txt')
    for x in range(i):
        url =  f"https://api.spoonacular.com/recipes/random?number=1&apiKey={k}"
        res = requests.get(url).json()
        try:
            recipe_titles.append(res['recipes'][0]['title'])
            recipe_images.append(res['recipes'][0]['image'])
            recipe_urls.append(res['recipes'][0]['spoonacularSourceUrl'])
            recipe_summaries.append(res['recipes'][0]['summary'])
        #Catch KeyError and return the message
        except KeyError as e:
            print('makeList(i) in api.py')
            info = res['message']
            return info
    info = [recipe_titles, recipe_images, recipe_urls, recipe_summaries]
    return info
    
def getLove(a, b):
    k = get_key('keys/key_loveCalculator.txt')
    url = "https://love-calculator.p.rapidapi.com/getPercentage"
    querystring = {"fname":a,"sname":b}
    headers = {
    'x-rapidapi-key': k, 
    'x-rapidapi-host':"love-calculator.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()['percentage']