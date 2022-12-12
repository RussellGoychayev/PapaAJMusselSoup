import requests

def get_key(s):
    with open(s) as f:
        k = f.readlines() #nasa api key
    key = k[0] #changes the key from a list to a string
    return key

def get_title():
    k = get_key("key_spoonacular.txt")
    print(k)
    url2 = f"https://api.spoonacular.com/recipes/716429/information?apiKey=7081bf709f0d44b7984587105086357f"
    res2 = requests.get(url2)
    recipies_api_summary = res2.json()['title']
    return recipies_api_summary

def get_photo():
    url2 = "https://api.spoonacular.com/recipes/716429/information?apiKey=7081bf709f0d44b7984587105086357f"
    res2 = requests.get(url2)
    recipies_api_summary = res2.json()['image']
    return recipies_api_summary

def get_url():
    url2 = "https://api.spoonacular.com/recipes/716429/information?apiKey=7081bf709f0d44b7984587105086357f"
    res2 = requests.get(url2)
    recipies_api_summary = res2.json()['sourceUrl']
    return recipies_api_summary

print(get_title())
print(get_photo())
print(get_url())
