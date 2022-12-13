import requests

def get_key(s):
    with open(s) as f:
        k = f.readlines() #nasa api key
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
    recipies_api_summary = res.json()['image']
    return recipies_api_summary

def get_url(x):
    url = f"https://api.spoonacular.com/recipes/{x}/information?apiKey=7081bf709f0d44b7984587105086357f"
    res = requests.get(url)
    recipies_api_summary = res.json()['sourceUrl']
    return recipies_api_summary

def search_recipe(query, l, u): #searches using query as a keyword and returns results l to u
    k = get_key('keys/key_edamam.txt')
    url =  "https://api.edamam.com/api/recipes/v2"
    res = requests.get(url, params={'type':'public', 'app_id':"904296dd", 'app_key':k, 'q': query})
    results = []
    while (l<u):
        results.append(res.json()['hits'][l]['recipe']['label']) #the index after hits is the x result (2 is second result from searching)
        l = l+1
    return results 
    
# populate list with randomly generated urls [title, image, and sourceUrl]
def makeList(i):
    recipeTitle = []
    recipeImage = []
    recipeUrl = []
    info = []
    k = get_key('keys/key_spoonacular.txt')
    for x in range(i):
        url =  f"https://api.spoonacular.com/recipes/random?number=1&apiKey={k}"
        res = requests.get(url)
        recipeTitle.append(res.json()['recipes'][0]['title'])
        recipeImage.append(res.json()['recipes'][0]['image'])
        recipeUrl.append(res.json()['recipes'][0]['spoonacularSourceUrl'])
    #print (res.json()['title'])
    #recipeImage.append(res.json()['image'])
    #recipeUrl.append(res.json()['sourceUrl'])
    info.append(recipeTitle)
    info.append(recipeImage)
    info.append(recipeUrl)
    return info

    

print(makeList(5))
