import requests

def get_key(s):
    with open(s) as f:
        k = f.readlines() #nasa api key
    key = k[0] #changes the key from a list to a string
    return key

def get_title():
    url = "https://api.spoonacular.com/recipes/716429/information?apiKey=7081bf709f0d44b7984587105086357f" #calling api with fstring doesn't work
    #print(url2)
    res = requests.get(url)
    recipies_api_summary = res.json()['title']
    return recipies_api_summary

def get_photo():
    url = "https://api.spoonacular.com/recipes/716429/information?apiKey=7081bf709f0d44b7984587105086357f"
    res = requests.get(url)
    recipies_api_summary = res.json()['image']
    return recipies_api_summary

def get_url():
    url = "https://api.spoonacular.com/recipes/716429/information?apiKey=7081bf709f0d44b7984587105086357f"
    res = requests.get(url)
    recipies_api_summary = res.json()['sourceUrl']
    return recipies_api_summary

