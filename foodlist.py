import requests
from bs4 import BeautifulSoup as Soup
import json
import string

def get_foodlist():
    url = "https://www.kpedu.fi/palvelut/ravintolat-ja-ruokalistat/menuetti-ja-pikkumenuetti-opiskelijaravintolat"
    data = requests.get(url)

    c = Soup(data.content, "html.parser")
    c = c.find_all("div", class_="content-expanded-list" )
    c = Soup(str(c), "html.parser")
    foods = c.find_all("p")
    h = ""
    for x in foods[1:]:
        h = h + x.get_text() + "\n"
    return h

def generate_jsonfile():
    try:
        h = get_foodlist()
        food_list = list(h.split("\n"))
        while True:
            try:
                food_list.remove("\xa0")
            except ValueError:
                break
        food_list.remove("")
        list_food = []
        date = ""
        data = {}
        for x in food_list:
            #print(list_food)
            if x.startswith("MAANANTAI"):
                
                list_food = []
                date = "ma"
                list_food.append(x)
            elif x.startswith("TIISTAI"):
                data.update({date:list_food})
                list_food = []
                date = "ti"
                list_food.append(x)
            elif x.startswith("KESKIVIIKKO"):
                data.update({date:list_food})
                list_food = []
                date = "ke"
                list_food.append(x)
            elif x.startswith("TORSTAI"):
                data.update({date:list_food})
                list_food = []
                date = "to"
                list_food.append(x)
            elif x.startswith("PERJANTA"):
                data.update({date:list_food})
                list_food = []
                date = "pe"
                list_food.append(x)
            else:
                list_food.append(x)
        data.update({date:list_food})
        #print("#############")
        #print(data)
        #data_json = json.dumps(data,indent=4).encode('utf8')
        #print(data_json.decode())
        with open("./data/foods.json",'w', encoding='utf8') as f: 
            json.dump(data, f, ensure_ascii=False) 
            #json.dump(data, f, indent=4, ensure_ascii=False)
        return "success"
    except Exception as e:
        print(e)
        return "error"

generate_jsonfile()