
#%% IMPORTS 
import requests
import re
import urllib.parse
import random
import time
import numpy as np
import json
import pandas as pd
import os

#%% Functions
def replace_commas_with_dots(text: str) -> str:
    return text.replace(",", ".")

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
        
def remove_prefix(s):
    return s.removeprefix("SkinBaron_").removeprefix("CsFloat_")


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

#%% CsFloat Database IDS
dict_ids_youpin = {}
dict_ids_youpin['Operation Breakout Weapon Case'] = 156
dict_ids_youpin['Clutch Case'] = 12
dict_ids_youpin['Winter Offensive Weapon Case'] = 45168
dict_ids_youpin['CS:GO Weapon Case'] = 47128
dict_ids_youpin['CS:GO Weapon Case 3'] = 48062
dict_ids_youpin['CS:GO Weapon Case 2'] = 46084
dict_ids_youpin['Operation Hydra Case'] = 50125
dict_ids_youpin['eSports 2014 Summer Case'] = 1117
dict_ids_youpin['Huntsman Weapon Case'] = 46475
dict_ids_youpin['Shattered Web Case'] = 1814
dict_ids_youpin['Operation Vanguard Weapon Case'] = 1177
dict_ids_youpin['eSports 2013 Winter Case'] = 1118
dict_ids_youpin['Chroma Case'] = 45444
dict_ids_youpin['Shadow Case'] = 368
dict_ids_youpin['Operation Bravo Case'] = 47514
dict_ids_youpin['Operation Riptide Case'] = 62265
dict_ids_youpin['Kilowatt Case'] = 108492
dict_ids_youpin['Revolution Case'] = 103158
dict_ids_youpin['CS20 Case'] = 9
dict_ids_youpin['Revolver Case'] = 38
dict_ids_youpin['Falchion Case'] = 125
dict_ids_youpin['Recoil Case'] = 102276
dict_ids_youpin['Operation Wildfire Case'] = 782
dict_ids_youpin['Gamma Case'] = 358
dict_ids_youpin['Snakebite Case'] = 53453
dict_ids_youpin['Spectrum Case'] = 1055
dict_ids_youpin['Gamma 2 Case'] = 369
dict_ids_youpin['Gallery Case'] = 109499
dict_ids_youpin['Fracture Case'] = 168
dict_ids_youpin['Horizon Case'] = 153
dict_ids_youpin['Operation Broken Fang Case'] = 6860
dict_ids_youpin['Glove Case'] = 77
dict_ids_youpin['Chroma 2 Case'] = 788
dict_ids_youpin['Prisma 2 Case'] = 8
dict_ids_youpin['Chroma 3 Case'] = 13
dict_ids_youpin['Operation Phoenix Weapon Case'] = 1176
dict_ids_youpin['Dreams & Nightmares Case'] = 101422
dict_ids_youpin['Prisma Case'] = 3
dict_ids_youpin['Spectrum 2 Case'] = 2
dict_ids_youpin['Danger Zone Case'] = 5
dict_ids_youpin['eSports 2013 Case'] = 57055
       
# %% Load Steam ids
# Open and read the JSON file
folder_path = 'C:\\Users\\Joao\\Desktop\\invesment_algorithm\\'

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


#%% Check Number of Cases Opened
case_openings_folder_path = 'C:\\Users\\Joao\\Desktop\\invesment_algorithm\\case_openings_records'
case_openings = {}  
case_times = {}

# Loop through all files in the folder
for file in os.listdir(case_openings_folder_path):
    if file.endswith(".csv"):  # Check if the file is a CSV
        file_path = os.path.join(case_openings_folder_path, file)
        
        # Read CSV into a DataFrame
        df = pd.read_csv(file_path)
        
        # Convert DataFrame to dictionary and store it
        case_openings_dict = df.to_dict(orient="records")
        
        for item in case_openings_dict:
            name = item['Case Name']
            opening_number = item['Unboxing Number']
            rarity = item['rarity']
            if rarity != 'Actively dropping' and rarity != 'Purchasable':
                if name in case_openings:
                    case_openings[name] += opening_number
                    case_times[name] += 1
                else:
                    case_openings[name] = opening_number
                    case_times[name] = 1 
for key in case_openings:
    case_openings[key] = case_openings[key]/case_times[key]


#%% Check Steam Listing (To see Supply)
# REQUEST Cs Data API
language = 'en'
url = f"https://bymykel.github.io/CSGO-API/api/{language}/all.json"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()    
else:
    print(f"Request failed with status code {response.status_code}")   



url = f"https://api.frankfurter.app/latest?amount=1&from=EUR&to=CNY"
response = requests.get(url)
eur_to_rmb = response.json()['rates']['CNY']


url_youpin = "https://api.youpin898.com/api/homepage/pc/goods/market/queryOnSaleCommodityList"
headers_youpin = {
  #  "accept": "application/json, text/plain, */*",
  #  "accept-encoding": "gzip, deflate, br, zstd",
  #  "accept-language": "pt,pt-BR;q=0.9,en-US;q=0.8,en;q=0.7",
  #  "app-version": "5.26.0",
  #  "apptype": "1",
  #  "appversion": "5.26.0",
    "authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlMjgyOTFiYTViZDU0ZDhjOTY5ZmIyNTk0YjJiYmI4MiIsIm5hbWVpZCI6IjEwOTg0MjQ3IiwiSWQiOiIxMDk4NDI0NyIsInVuaXF1ZV9uYW1lIjoiWVAwMDEwOTg0MjQ3IiwiTmFtZSI6IllQMDAxMDk4NDI0NyIsInZlcnNpb24iOiIycG4iLCJuYmYiOjE3NDE4ODYwOTUsImV4cCI6MTc0Mjc1MDA5NSwiaXNzIjoieW91cGluODk4LmNvbSIsImRldmljZUlkIjoiNjljMWI3ZGQtZjBlNC00N2UyLTg1Y2ItYmM4NTY4MmRkNWQwIiwiYXVkIjoidXNlciJ9.E_i38wj5tQ-FoOCf3IuAsOHZwGI7yfh-NSM6cVZ7590",
    # "b3": "5959cd9785c64070895f9e87a95d68d5-d6d8ae008122d10d-1",
    "content-type": "application/json",
    #"deviceid": "69c1b7dd-f0e4-47e2-85cb-bc85682dd5d0",
    #"dnt": "1",
    "origin": "https://www.youpin898.com",
    "platform": "pc",
    #"priority": "u=1, i",
    #"referer": "https://www.youpin898.com/",
    #"sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    #"sec-ch-ua-mobile": "?0",
    #"sec-ch-ua-platform": '"Windows"',
    #"sec-fetch-dest": "empty",
    #"sec-fetch-mode": "cors",
    #"sec-fetch-site": "same-site",
    #"sec-gpc": "1",
    #"secret-v": "h5_v1",
    #"traceparent": "00-5959cd9785c64070895f9e87a95d68d5-d6d8ae008122d10d-01",
    #"tracestate": "rum=v2&browser&hwztx6svg3@74450dd02fdbfcd&9fc99e8342a24e2cb929687c08ba0267&uid_kbgg400qbsa4doh1",
    "uk": "5FDHeFgpuYgc7liDrGbnZWeltwHWlqmQUiFGholkimoiivDuCfwXyMNLEQl2gCD1S",
    #'uk': "5FGLeI4yhHqLrO3u0IJkL3KRlCE3iRzS7t0ufCyXGpwwJSbSoV4rkttm7LDksST1M",
    #"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

payload_youpin = {
    "gameId": "730",
    "listType": "10",
}

#%% Get Prices SkinBaron and CsFloat

url_fx_csfloat = f"https://csfloat.com/api/v1/meta/exchange-rates"
response_fx_csfloat = requests.get(url_fx_csfloat)
fx_conversion = response_fx_csfloat.json()

api_key_csfloat = "6VTrcNP13k2EfBW_XN3gFO0aK0r9gt8u"
headers_csfloat = {
    "Authorization": f"{api_key_csfloat}",  # Assuming Bearer Token authentication
    "Accept": "application/json"  # Optional: Ensures response is JSON
}


# Get Cases
price_data = {}
case_listings = {}
case_price = {}
case_buy_order_price = {}
for key, item in data.items():
    if ('crate' in key) and data[key]['type'] == 'Case' and item['name'] in dict_ids_steam:
        print("--> " + str(data[key]['name']))
        item = item
        name = item['name']
        
        # YouPin
        num_tries = 0
        while True:
            try:
                payload_youpin["templateId"] = str(dict_ids_youpin[item['name']])
                response_youpin = requests.post(url_youpin, headers=headers_youpin, json=payload_youpin)
                data_youpin = response_youpin.json()
                item['price_youpin'] = float(data_youpin['Data'][0]['price'])/eur_to_rmb
                break
            except Exception:
                print("Error trying to get YouPin Info")
            wait_time = random.uniform(5*num_tries + 5, 5*num_tries + 6)
            time.sleep(wait_time)
            num_tries += 1

        # Steam
        num_tries = 0
        while True:
            try:
                steam_id = dict_ids_steam[item['name']]
                url_steam = "https://steamcommunity.com/market/itemordershistogram?country=PT&language=english&currency=3&item_nameid=" + str(steam_id)
                response_steam_listing = requests.get(url_steam)
                response_steam_listing.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
                data_steam_listing = response_steam_listing.json()
                
                # Number Listings
                match = re.search(r'>(\d+)<', data_steam_listing['sell_order_summary'])
                if match:
                    number_listings = float(match.group(1))
                    case_listings[name] = number_listings
                    print("Number of listings: " + str(case_listings[name]))
                  
                # Price  
                matches = re.findall(r'>([^<]+)<', data_steam_listing['sell_order_summary'])
                len_matches = len(matches)
                i = 0
                while i < len(matches):
                    matches[i] = matches[i].replace('--', '00').replace(',', '.').strip('€').strip()
                    try:
                        matches[i] = float(matches[i])
                    except:
                        del matches[i]
                        i = i - 1
                    i = i + 1
                if match:
                    case_price[name] = matches[1]

                # Buy order price
                case_buy_order_price[name] = data_steam_listing['buy_order_graph'][0][0] + 0.01
                
                break  # Exit loop if successful
            except Exception:
                print("Error trying to get Steam Info")
       
        item['price_steam'] = case_price[name]
        
        
        # Get price Skinbaron
        num_tries = 0
        while True:
            try:
                skinbaron_id = dict_ids_skinbaron[item['name']]
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

                item['price_skinbaron'] = price_skinbaron
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
                csfloat_id = dict_ids_csfloat[item['name']]
                url_csfloat = "https://csfloat.com/api/v1/listings?limit=40&def_index=" + str(csfloat_id)
                response_csfloat = requests.get(url_csfloat, headers = headers_csfloat)
                response_csfloat.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
                data_csfloat = response_csfloat.json()
                price_csfloat_dollar = data_csfloat['data'][0]['price']  # Parse JSON response
                eur_conversion = fx_conversion['data']['eur']
                price_csfloat = (np.ceil(price_csfloat_dollar*eur_conversion)/100)
                price_csfloat = price_csfloat # Adjust based on taxes to input money into the website
                item['price_csfloat'] = price_csfloat
                break  # Exit loop if successful
            except Exception:
                print("Error trying to get CsFloat Price") 
            
            wait_time = random.uniform(5*num_tries + 5, 5*num_tries + 6)
            time.sleep(wait_time)
            num_tries += 1

        price_data[name] = {}
        price_data[name]['price_steam'] = item['price_steam']
        price_data[name]['price_skinbaron'] = item['price_skinbaron']
        price_data[name]['price_csfloat'] = item['price_csfloat'] 
        price_data[name]['price_youpin'] = item['price_youpin']
        price_data[name]['price_steam_buy_order'] = case_buy_order_price[name]

        
        print("Steam Price: " + str(price_data[name]['price_steam']))
        print("Steam Price Buy Order: " + str(price_data[name]['price_steam_buy_order']))
        print("Skinbaron Price: " + str(price_data[name]['price_skinbaron']))
        print("Csfloat Price: " + str(price_data[name]['price_csfloat']))
        print("YouPin Price: " + str(price_data[name]['price_youpin']))
        wait_time = random.uniform(20, 30)
        time.sleep(wait_time)
        

# %% Calculate Best Investment Ratio
common_keys = case_openings.keys() & dict_ids_csfloat.keys() & dict_ids_skinbaron.keys()
best_investment = {}
for key in common_keys:
    best_investment[key] = case_openings[key]/(case_listings[key]*(case_price[key]**1.1))

# Order Best Skinbaron -> Steam Skin
best_investment = dict(sorted(best_investment.items(), key=lambda item: item[1], reverse=True))
print(best_investment)

# %%
buy_steam_sell_csfloat = {}
for name in price_data:
    buy_steam_sell_csfloat[name] = price_data[name]['price_csfloat']/price_data[name]['price_steam_buy_order']
buy_steam_sell_csfloat_dict = dict(sorted(buy_steam_sell_csfloat.items(), key=lambda item: item[1], reverse=True))
best_key_buy_steam_sell_csfloat = list(buy_steam_sell_csfloat_dict.items())[0][0]
best_price_buy_steam_sell_csfloat = list(buy_steam_sell_csfloat_dict.items())[0][1]
print(best_key_buy_steam_sell_csfloat)
print(best_price_buy_steam_sell_csfloat)

# %% Check ratios between Steam and SkinBaron/CsFloat
best_website_to_steam = {}
for name in price_data:
    price_data[name]['price_steam_after_taxes'] = to_seller_price_cents(int(price_data[name]['price_steam']*100))/100
    price_data[name]['skinbaron_conversion'] = price_data[name]['price_steam_after_taxes']/price_data[name]['price_skinbaron']
    price_data[name]['csfloat_conversion_no_tax'] = price_data[name]['price_steam']/(price_data[name]['price_csfloat']*1.0432)
    price_data[name]['skinbaron_conversion_no_tax'] = price_data[name]['price_steam']/price_data[name]['price_skinbaron']
    price_data[name]['csfloat_conversion'] = price_data[name]['price_steam_after_taxes']/(price_data[name]['price_csfloat']*1.0432)
    best_website_to_steam["SkinBaron_" + name] = price_data[name]['price_steam_after_taxes']/price_data[name]['price_skinbaron']
    best_website_to_steam["CsFloat_" + name] = price_data[name]['price_steam_after_taxes']/(price_data[name]['price_csfloat']*1.0432)
best_website_to_steam = dict(sorted(best_website_to_steam.items(), key=lambda item: item[1], reverse=True))

best_key_website_to_steam = list(best_website_to_steam.items())[0][0]
best_website_to_steam_conversion = list(best_website_to_steam.items())[0][1]


print("--------------------------------------------------------------------------------------------")
print(" Best Conversion Website -> Steam ----------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")
i = 0
for key in best_website_to_steam:
    if i < 5:
        print("--------------------------------------------------------------------------------------------")
        print("--> Case: " + str(key))
        print("Percentage Conversion: " + str(best_website_to_steam[key]))
        print("Price Steam: " + str(price_data[remove_prefix(key)]['price_steam']))
        print("Price Steam after taxes: " + str(price_data[remove_prefix(key)]['price_steam_after_taxes']))
        
        if 'SkinBaron' in key:
            print("Price Website: " + str(price_data[remove_prefix(key)]['price_skinbaron']))
        elif 'CsFloat' in key:
            print("Price Website: " + str(price_data[remove_prefix(key)]['price_csfloat']))
    i += 1
   

# %% Check for each best investment the best thing to do (Or buy in website, or the case to buy and sell on steam)
print("--------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")
print("Best Website -> Steam Conversion: " + str(best_website_to_steam_conversion))
print("Price: " + str(best_website_to_steam_conversion))

print("--------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")
i = 0
for key in best_investment:
    if i < 30:
        print("--> Buy " + key)
        print("Score: " + str(best_investment[key]))
        if (best_website_to_steam_conversion > price_data[key]['csfloat_conversion_no_tax'] and\
            best_website_to_steam_conversion > price_data[key]['skinbaron_conversion_no_tax']):
            print("--> Buy " + str(best_key_website_to_steam) + " and sell on steam. Then buy order " + str(key))
            if 'SkinBaron' in best_key_website_to_steam:
                money_buy = price_data[remove_prefix(best_key_website_to_steam)]['price_skinbaron']
                first_sell = price_data[remove_prefix(best_key_website_to_steam)]['price_steam_after_taxes'] 
                conversion_real_money = 100*((to_seller_price_cents(100*first_sell)/100 * 0.85 * 0.95) - money_buy)/money_buy
                print("Conversion again into real money: " + str(conversion_real_money))
            elif 'CsFloat' in best_key_website_to_steam:
                money_buy = price_data[remove_prefix(best_key_website_to_steam)]['price_csfloat'] 
                first_sell = price_data[remove_prefix(best_key_website_to_steam)]['price_steam_after_taxes'] 
                conversion_real_money = 100*((to_seller_price_cents(100*first_sell)/100 * 0.85 * 0.95) - money_buy)/money_buy
                print("Conversion again into real money: " + str(conversion_real_money))
        else:
            if price_data[key]['csfloat_conversion_no_tax'] > price_data[key]['skinbaron_conversion_no_tax']:
                conversion_real_money = 100*(price_data[key]['price_steam_after_taxes']*0.85*0.95 - price_data[key]['price_csfloat']*1.0432)/(price_data[key]['price_csfloat']*1.0432)
                print("--> Buy " + str(key) + " at CsFloat")
                print("Conversion again into real money: " + str(conversion_real_money))
            else:
                conversion_real_money = 100*(price_data[key]['price_steam_after_taxes']*0.85*0.95 - price_data[key]['price_skinbaron'])/(price_data[key]['price_skinbaron'])
                print("--> Buy " + str(key) + " at SkinBaron")
                print("Conversion again into real money: " + str(conversion_real_money))
                
        print("CsFloat Conversion no tax:" + str(price_data[key]['csfloat_conversion_no_tax']))
        print("SkinBaron Conversion no tax:" + str(price_data[key]['skinbaron_conversion_no_tax']))
        print("Price SkinBaron " + str(price_data[key]['price_skinbaron']))
        print("Price CsFloat " + str(price_data[key]['price_csfloat']))
        print("--------------------------------------------------------------------------------------------")
        
    i += 1
    
    
#%% FAzer Youpin Steam -> youpin balance conversion

# and then buy the thing at youpin