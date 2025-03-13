
#%% IMPORTS 
import requests
import re
import urllib.parse
import random
import time
import numpy as np
import json

#%% SkinBaron Database IDS
dict_ids_skinbaron = {}
dict_ids_skinbaron['Operation Breakout Weapon Case'] = 256
dict_ids_skinbaron['Clutch Case'] = 767005
dict_ids_skinbaron['Winter Offensive Weapon Case'] = 223
dict_ids_skinbaron['CS:GO Weapon Case'] = 923
dict_ids_skinbaron['CS:GO Weapon Case 3'] = 5355
dict_ids_skinbaron['CS:GO Weapon Case 2'] = 927
dict_ids_skinbaron['Operation Hydra Case'] = 136909
dict_ids_skinbaron['eSports 2014 Summer Case'] = 4300
dict_ids_skinbaron['Huntsman Weapon Case'] = 224
dict_ids_skinbaron['Shattered Web Case'] = 7191070
dict_ids_skinbaron['Operation Vanguard Weapon Case'] = 373
dict_ids_skinbaron['eSports 2013 Winter Case'] = 222
dict_ids_skinbaron['Chroma Case'] = 225
dict_ids_skinbaron['Shadow Case'] = 208
dict_ids_skinbaron['Operation Bravo Case'] = 257
dict_ids_skinbaron['Operation Riptide Case'] = 36318587
dict_ids_skinbaron['Kilowatt Case'] = 48702856
dict_ids_skinbaron['Revolution Case'] = 43352341
dict_ids_skinbaron['CS20 Case'] = 5882447
dict_ids_skinbaron['Revolver Case'] = 216
dict_ids_skinbaron['Falchion Case'] = 197
dict_ids_skinbaron['Recoil Case'] = 40781303
dict_ids_skinbaron['Operation Wildfire Case'] = 323
dict_ids_skinbaron['Gamma Case'] = 230
dict_ids_skinbaron['Snakebite Case'] = 33444419
dict_ids_skinbaron['Spectrum Case'] = 89914
dict_ids_skinbaron['Gamma 2 Case'] = 726
dict_ids_skinbaron['Gallery Case'] = 55347776
dict_ids_skinbaron['Fracture Case'] = 24322063
dict_ids_skinbaron['Horizon Case'] = 1263067
dict_ids_skinbaron['Operation Broken Fang Case'] = 28950707
dict_ids_skinbaron['Glove Case'] = 29334
dict_ids_skinbaron['Chroma 2 Case'] = 214
dict_ids_skinbaron['Prisma 2 Case'] = 15870576
dict_ids_skinbaron['Chroma 3 Case'] = 209
dict_ids_skinbaron['Operation Phoenix Weapon Case'] = 221
dict_ids_skinbaron['Dreams & Nightmares Case'] = 37707469
dict_ids_skinbaron['Prisma Case'] = 2514665
dict_ids_skinbaron['Spectrum 2 Case'] = 274032
dict_ids_skinbaron['Danger Zone Case'] = 1732971
dict_ids_skinbaron['eSports 2013 Case'] = 924

#%% CsFloat Database IDS
dict_ids_csfloat = {}
dict_ids_csfloat['Operation Breakout Weapon Case'] = 4018
dict_ids_csfloat['Clutch Case'] = 4471
dict_ids_csfloat['Winter Offensive Weapon Case'] = 4009
dict_ids_csfloat['CS:GO Weapon Case'] = 4001
dict_ids_csfloat['CS:GO Weapon Case 3'] = 4010
dict_ids_csfloat['CS:GO Weapon Case 2'] = 4004
dict_ids_csfloat['Operation Hydra Case'] = 4352
dict_ids_csfloat['eSports 2014 Summer Case'] = 4019
dict_ids_csfloat['Huntsman Weapon Case'] = 4017
dict_ids_csfloat['Shattered Web Case'] = 4620
dict_ids_csfloat['Operation Vanguard Weapon Case'] = 4029
dict_ids_csfloat['eSports 2013 Winter Case'] = 4005
dict_ids_csfloat['Chroma Case'] = 4061
dict_ids_csfloat['Shadow Case'] = 4138
dict_ids_csfloat['Operation Bravo Case'] = 4003
dict_ids_csfloat['Operation Riptide Case'] = 4790
dict_ids_csfloat['Kilowatt Case'] = 4904
dict_ids_csfloat['Revolution Case'] = 4880
dict_ids_csfloat['CS20 Case'] = 4669
dict_ids_csfloat['Revolver Case'] = 4186
dict_ids_csfloat['Falchion Case'] = 4091
dict_ids_csfloat['Recoil Case'] = 4846
dict_ids_csfloat['Operation Wildfire Case'] = 4187
dict_ids_csfloat['Gamma Case'] = 4236
dict_ids_csfloat['Snakebite Case'] = 4747
dict_ids_csfloat['Spectrum Case'] = 4351
dict_ids_csfloat['Gamma 2 Case'] = 4281
dict_ids_csfloat['Gallery Case'] = 7003
dict_ids_csfloat['Fracture Case'] = 4698
dict_ids_csfloat['Horizon Case'] = 4482
dict_ids_csfloat['Operation Broken Fang Case'] = 4717
dict_ids_csfloat['Glove Case'] = 4288
dict_ids_csfloat['Chroma 2 Case'] = 4089
dict_ids_csfloat['Prisma 2 Case'] = 4695
dict_ids_csfloat['Chroma 3 Case'] = 4233
dict_ids_csfloat['Operation Phoenix Weapon Case'] = 4011
dict_ids_csfloat['Dreams & Nightmares Case'] = 4818
dict_ids_csfloat['Prisma Case'] = 4598
dict_ids_csfloat['Spectrum 2 Case'] = 4403
dict_ids_csfloat['Danger Zone Case'] = 4548
dict_ids_csfloat['eSports 2013 Case'] = 4002

# %% Steam ids
# Open and read the JSON file
folder_path = 'C:\\Users\\Joao\\Desktop\\invesment_algorithm\\'

import json

# Load JSON file
with open(folder_path + 'steam_ids.json', "r", encoding="utf-8") as file:
    dict_ids_steam_aux = json.load(file)


dict_ids_steam = {}
for key in dict_ids_csfloat:
    if key == 'Kilowatt Case':
        dict_ids_steam[key] = 176413986
    elif key == 'Revolution Case':
        dict_ids_steam[key] = 176358765
    elif key == 'Gallery Case':
        dict_ids_steam[key] = 176460428
    else:
        dict_ids_steam[key] = dict_ids_steam_aux[key]
del dict_ids_steam_aux


#%% Functions
def format_string(input_string):
    return urllib.parse.quote(input_string)

def extract_lowest_price(base_url, endpoint):
    full_url = f"{base_url}{endpoint}"
    response = requests.get(full_url)
    
    if response.status_code == 200:
        data = response.text
        match = re.search(r'"lowest_price":"([^"]+)"', data)
        
        if match:
            lowest_price = re.sub(r'[^0-9,]+', '', match.group(1))
            return lowest_price
    
    return None

def replace_commas_with_dots(text: str) -> str:
    return text.replace(",", ".")

def to_buyer_price_cents(seller_price_cents):
    s = seller_price_cents
    return s + max(1, int(s * 0.05)) + max(1, int(s * 0.10))

def to_seller_price_cents(buyer_price_cents):
    if(buyer_price_cents<=3):
        return 0
    else:
        b = buyer_price_cents
        s = 1
        while s < b:
            b_candidate = to_buyer_price_cents(s)
            if b == b_candidate:
                return s
            elif b < b_candidate:
                return s - 1
            s += 1
        raise ValueError("Couldn't calculate seller price of buyer price {} cents.".format(b))
        
#%% MAin
# Steam API
steam_api = "https://steamcommunity.com/market/priceoverview/?currency=3&appid=730&market_hash_name="
item_api = 'https://steamcommunity.com/market/listings/730/'

# Get conversion Csfloat
url_fx_csfloat = f"https://csfloat.com/api/v1/meta/exchange-rates"
response_fx_csfloat = requests.get(url_fx_csfloat)
fx_conversion = response_fx_csfloat.json()

api_key_csfloat = "6VTrcNP13k2EfBW_XN3gFO0aK0r9gt8u"
headers_csfloat = {
    "Authorization": f"{api_key_csfloat}",  # Assuming Bearer Token authentication
    "Accept": "application/json"  # Optional: Ensures response is JSON
}


# REQUEST Cs Data API
language = 'en'
url = f"https://bymykel.github.io/CSGO-API/api/{language}/all.json"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()    
else:
    print(f"Request failed with status code {response.status_code}")   


 
# Get Cases
data_crates = {}
price_data = {}
for key, item in data.items():
    if ('crate' in key) and data[key]['type'] == 'Case':
        print("--> " + str(data[key]['name']))
        data_crates[key] = item
        name = data_crates[key]['name']
        
        # Get price from steam api
        name_formated = format_string(data_crates[key]['name'])
        item_api_completed = item_api + name_formated
        num_tries = 0
        while True:
            try:
                match = re.search(r".*730/(.*)", item_api_completed)
                endpoint = match.group(1)
                price = extract_lowest_price(steam_api, endpoint)
                price = replace_commas_with_dots(str(price))  # Convert to string
                data_crates[key]['price_steam'] = float(price)  # Convert to float
                break  # Exit loop if successful
            except Exception:
                print("Error trying to get Steam Price")
            
            wait_time = random.uniform(5*num_tries, 5*num_tries + 1)
            time.sleep(wait_time)
            num_tries += 1
            
        # Get price Skinbaron
        num_tries = 0
        while True:
            try:
                skinbaron_id = dict_ids_skinbaron[data_crates[key]['name']]
                data_skinbaron = requests.get('https://skinbaron.de/api/v2/Offer?metaOfferId=' + str(skinbaron_id))
                price_skinbaron_tradelock = data_skinbaron.json()['formattedLowestPriceTradeLocked']
                price_skinbaron_no_tradelock = data_skinbaron.json()['formattedLowestPrice']
                
                match = re.search(r"\d+\.\d+", price_skinbaron_tradelock)
                price_skinbaron_tradelock = float(match.group())
                
                match = re.search(r"\d+\.\d+", price_skinbaron_no_tradelock)
                price_skinbaron_no_tradelock = float(match.group())
                
                price_skinbaron = min(price_skinbaron_tradelock, price_skinbaron_no_tradelock)
                if price_skinbaron < 0.01:
                    price_skinbaron = max(price_skinbaron_tradelock, price_skinbaron_no_tradelock)

                data_crates[key]['price_skinbaron'] = price_skinbaron
                break  # Exit loop if successful
            except Exception:
                print("Error trying to get SkinBaron Price")
            
            wait_time = random.uniform(5*num_tries + 5, 5*num_tries + 6)
            time.sleep(wait_time)
            num_tries += 1
        
        # Get price CsFloat
        num_tries = 0
        while True:
            try:
                csfloat_id = dict_ids_csfloat[data_crates[key]['name']]
                url_csfloat = "https://csfloat.com/api/v1/listings?limit=40&def_index=" + str(csfloat_id)
                response_csfloat = requests.get(url_csfloat, headers = headers_csfloat)
                response_csfloat.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
                data_csfloat = response_csfloat.json()
                price_csfloat_dollar = data_csfloat['data'][0]['price']  # Parse JSON response
                eur_conversion = fx_conversion['data']['eur']
                price_csfloat = (np.ceil(price_csfloat_dollar*eur_conversion)/100)
                price_csfloat = price_csfloat*1.0432 # Adjust based on taxes to input money into the website
                data_crates[key]['price_csfloat'] = price_csfloat
                break  # Exit loop if successful
            except Exception:
                print("Error trying to get SkinBaron Price")
            
            wait_time = random.uniform(5*num_tries + 5, 5*num_tries + 6)
            time.sleep(wait_time)
            num_tries += 1

        price_data[name] = {}
        price_data[name]['price_steam'] = data_crates[key]['price_steam']
        price_data[name]['price_skinbaron'] = data_crates[key]['price_skinbaron']
        price_data[name]['price_csfloat'] = data_crates[key]['price_csfloat']
        
        
        print("Steam Price: " + str(price_data[name]['price_steam']))
        print("Skinbaron Price: " + str(price_data[name]['price_skinbaron']))
        print("Csfloat Price: " + str(price_data[name]['price_csfloat']))
        wait_time = random.uniform(5, 6)
        time.sleep(wait_time)
        
        # Get Listings Case
        num_tries = 0
        while True:
            try:
                steam_id = dict_ids_steam[data_crates[key]['name']]
                url_steam = "https://steamcommunity.com/market/itemordershistogram?country=PT&language=english&currency=3&item_nameid=" + str(steam_id)
                response_steam_listing = requests.get(url_steam)
                response_steam_listing.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
                data_steam_listing = response_steam_listing.json()
                match = re.search(r'>(\d+)<', data_steam_listing['sell_order_summary'])
                if match:
                    number_listings = match.group(1)
                    print(number_listings)
                break  # Exit loop if successful
            except Exception:
                print("Error trying to get SkinBaron Price")
            
            wait_time = random.uniform(5*num_tries + 5, 5*num_tries + 6)
            time.sleep(wait_time)
            num_tries += 1
        
        wait_time = random.uniform(5, 6)
        time.sleep(wait_time)
        

# Get Steam/PRice
best_website_to_steam = {}
for name in price_data:
    price_data[name]['price_steam_after_taxes'] = to_seller_price_cents(price_data[name]['price_steam']*100)/100
    price_data[name]['skinbaron_conversion'] = price_data[name]['price_steam_after_taxes']/price_data[name]['price_skinbaron']
    price_data[name]['csfloat_conversion_no_tax'] = price_data[name]['price_steam']/price_data[name]['price_csfloat']
    price_data[name]['skinbaron_conversion_no_tax'] = price_data[name]['price_steam']/price_data[name]['price_skinbaron']
    price_data[name]['csfloat_conversion'] = price_data[name]['price_steam_after_taxes']/price_data[name]['price_csfloat']
    best_website_to_steam["SkinBaron_" + name] = price_data[name]['price_steam_after_taxes']/price_data[name]['price_skinbaron']
    best_website_to_steam["CsFloat_" + name] = price_data[name]['price_steam_after_taxes']/price_data[name]['price_csfloat']
    
# Order Best Skinbaron -> Steam Skin
best_website_to_steam = dict(sorted(best_website_to_steam.items(), key=lambda item: item[1], reverse=True))

def remove_prefix(s):
    return s.removeprefix("SkinBaron_").removeprefix("CsFloat_")

print("---- Results ------")
i = 0
for key in best_website_to_steam:
    if i < 10:
        print("--> Case: " + str(key))
        print("Percentage Conversion: " + str(best_website_to_steam[key]))
        print("Price Steam: " + str(price_data[remove_prefix(key)]['price_steam']))
        print("Price Steam after taxes: " + str(price_data[remove_prefix(key)]['price_steam_after_taxes']))
        
        if 'SkinBaron' in key:
            print("Price Website: " + str(price_data[remove_prefix(key)]['price_skinbaron']))
        elif 'CsFloat' in key:
            print("Price Website: " + str(price_data[remove_prefix(key)]['price_csfloat']))
    i += 1



