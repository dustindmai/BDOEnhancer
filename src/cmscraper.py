'''
import requests
def fetch_enhanceable_accessories():
    ## Obtain a list of enhanceable accessories
    # Category number for accessories
    main_category = 20

    # API Endpoint
    url = 'https://api.arsha.io/v2/na/GetWorldMarketList'

    # Params for API request

    params = {
        "mainCategory": main_category,
        #"subCategory": 1,
        "lang" : "en"
    }
    # Get request
    response = requests.get(url, params = params)
    # Check if request is successful
    if response.status_code == 200:
        accessories = response.json()
    else:
        print(f"Error: Unable to fetch data (Status Code: {response.status_code})\n")

    ## Market Prices
    # API endpoint for fetching market data
    url = "https://api.arsha.io/v2/na/GetMarketPriceInfo"
    enhanceables = []
    for accessory in accessories:
        # Filter out manos accessories, accessories that aren't worth much, and accessories with low stock
        if "Manos" in accessory['name'] or accessory['basePrice'] < 4_000_000 or accessory['currentStock'] < 30:
            continue
        # Average out the last 10 trade prices, and include in accessory information
        prices =[]
        for enhanceLevel in range(5):
            params = {
                "id": accessory['id'],  # Item IDs
                "sid": enhanceLevel,     # Enhancement Level
                "lang": "en"  # Language parameter
            }

            # Send a GET request to the API
            response = requests.get(url, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON data
                data = response.json()
                # If there are more than 10 purchases, get the last 10 trade prices and average it
                if len(data['history']) >= 10:
                    avg = sum(list(data['history'].values())[-10:])/10
                # Otherwise average all the trade prices
                else:
                    avg = sum(data['history'].values())/len(data['history'])
                prices.append(int(avg))
            else:
                break
        # Only include accessories that have all 5 enhancement levels
        if len(prices) == 5:
            accessory['prices'] = prices
            enhanceables.append(accessory)
    return enhanceables
'''

import requests
import json
# API Endpoints
WORLD_MARKET_LIST_URL = 'https://api.arsha.io/v2/na/GetWorldMarketList'
MARKET_PRICE_INFO_URL = 'https://api.arsha.io/v2/na/GetMarketPriceInfo'
ITEM_DATABASE_URL = 'https://api.arsha.io/util/db'
ITEM_URL = 'https://api.arsha.io/v1/na/item'
# 1. Fetch accessories from the API
def fetch_accessories(main_category=20, lang='en'):
    params = {
        "mainCategory": main_category,
        "lang": lang
    }

    response = requests.get(WORLD_MARKET_LIST_URL, params=params)

    if response.status_code == 200:
        accessories = response.json()
        for accessory in accessories:
            params ={
                "id": accessory['id']
            }
            response = requests.get(ITEM_DATABASE_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                accessory['grade'] = data['grade']
            else:
                Exception(f"Error: Unable to fetch data (Status Code: {response.status_code})")
            
            params = {
                "id": accessory['id'],
                "region": "na"
            }
            response = requests.get(ITEM_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                maxEnhance = len(data['resultMsg'].split('|'))-1
                accessory['maxEnhance'] = maxEnhance
        return accessories
    else:
        raise Exception(f"Error: Unable to fetch data (Status Code: {response.status_code})")



# 3. Fetch enhancement prices for a given accessory by enhancement levels (0-4)
def fetch_enhancement_prices(accessory_id, max_enhancement_level, lang='en'):
    prices = []
        
    for enhanceLevel in range(max_enhancement_level+1):
        params = {
            "id": accessory_id,
            "sid": enhanceLevel,
            "lang": lang
        }

        response = requests.get(MARKET_PRICE_INFO_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            # If there are more than 10 purchases, get the last 10 trade prices and average it
            if len(data['history']) >= 10:
                avg = sum(list(data['history'].values())[-10:]) / 10
            else:
                avg = sum(data['history'].values()) / len(data['history'])
            prices.append(int(avg))
        else:
            break  # Stop fetching if an error occurs
    return prices


# 4. Run the full scraping and filtering process
def get_enhanceable_accessories():
    accessories = fetch_accessories()
    for accessory in accessories:
        prices = fetch_enhancement_prices(accessory['id'], accessory['maxEnhance'])
        accessory['prices'] = prices
    return accessories