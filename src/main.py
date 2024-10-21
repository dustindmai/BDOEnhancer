import os
import json
import time
from cmscraper import get_enhanceable_accessories
from enhancement_sim import simulate_enhancement, fs_to_rate

levels={0:"base", 1:"pri", 2:"duo", 3:"tri", 4:"tet", 5:"pen"}
grades={0: "white", 1:"green", 2:"blue", 3:"yellow"}
def startup():
    file_path = os.path.join('src', 'utils', 'accessories.json')
    current_time = time.time()
    if not os.path.exists(file_path) or current_time - os.path.getmtime(file_path) > 24 * 60 * 60:
        t = time.time()
        print("Accessories data is outdated. Fetching new data...")
        accessories = get_enhanceable_accessories()
        with open(file_path, 'w') as file:
            json.dump(accessories, file, indent=4)
        print(f"Accessories data has been updated. Time taken: {time.time() - t:.2f} seconds ")
    else:
        print("Accessories data is up to date.")
    with open(file_path, 'r') as file:
        data = json.load(file)
        
        
        
    return data

def filter(accessory):
    return (
        accessory['maxEnhance'] != 5 or
        accessory['grade'] != 3 or
        'Manos' in accessory['name']
    )

def main():
    accessories = startup()
    trials = 100_000
    fs= [18,40,44,110,200]
    rate = [fs_to_rate(fs[i], i) for i in range(len(fs))]
    start = 0
    stop = 3
    current_time = time.time()
     # BASIC ARRAY/DICTIONARY
    
    for j in range(len(accessories)):
        if filter(accessories[j]):
            continue
        currGain = 0
        currLoss = 0
        for i in range(trials):
            [loss, gain] = simulate_enhancement(accessories[j], start, stop, rate)
            currGain += gain
            currLoss += loss
        print(f"Average gain for {accessories[j]['name']} from {levels[start]} to {levels[stop]} over {trials} trials: {currGain/trials:,.2f}")
        print(f"Average loss for {accessories[j]['name']} from {levels[start]} to {levels[stop]} over {trials} trials: {currLoss/trials:,.2f}")
        print(f"Average % profit for {accessories[j]['name']} from {levels[start]} to {levels[stop]}: {100 * (currGain/currLoss - 1):.2f}%")


    print(f"Time taken: {time.time() - current_time:.2f} seconds.")
    
    
if __name__ in {"__main__", "__mp_main__"}:
    main()
