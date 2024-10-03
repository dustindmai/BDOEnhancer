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