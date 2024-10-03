import random
import cmscraper
import json

def saveToJSON(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to {filename}")

def enhance(chance):
    chance = int(chance * 100_000)
    bound = 10_000_000
    return random.randint(0, bound) <= chance

