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

# API Endpoints
WORLD_MARKET_LIST_URL = 'https://api.arsha.io/v2/na/GetWorldMarketList'
MARKET_PRICE_INFO_URL = 'https://api.arsha.io/v2/na/GetMarketPriceInfo'


# 1. Fetch accessories from the API
def fetch_accessories(main_category=20, lang='en'):
    params = {
        "mainCategory": main_category,
        "lang": lang
    }

    response = requests.get(WORLD_MARKET_LIST_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: Unable to fetch data (Status Code: {response.status_code})")


# 2. Filter accessories (e.g., remove Manos accessories, those with low stock, or low base price)
def filter_accessories(accessories, min_price=0, min_stock=0):
    filtered = []
    for accessory in accessories:
        if "Manos" in accessory['name']:
            continue
        if accessory['basePrice'] < min_price:
            continue
        if accessory['currentStock'] < min_stock:
            continue
        filtered.append(accessory)

    return filtered


# 3. Fetch enhancement prices for a given accessory by enhancement levels (0-4)
def fetch_enhancement_prices(accessory_id, max_enhancement_level=5, lang='en'):
    prices = []
    for enhanceLevel in range(max_enhancement_level):
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
    filtered_accessories = filter_accessories(accessories)

    enhanceables = []
    for accessory in filtered_accessories:
        prices = fetch_enhancement_prices(accessory['id'])
        if prices[4] > 1_000_000:  # Only include accessories that have all 5 enhancement levels
            accessory['prices'] = prices
            enhanceables.append(accessory)

    return enhanceables