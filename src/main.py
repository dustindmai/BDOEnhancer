import os
import json
import time
from cmscraper import get_enhanceable_accessories
from enhancement_sim import simulate_enhancement, fs_to_rate
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
        accessories = json.load(file)
    return accessories


def main():
    accessories = startup()
    
    
    trials = 1000
    fs= [18,40,44,110,200]
    rate = [fs_to_rate(fs[i], i) for i in range(len(fs))]
    start = 0
    stop = 5
    for j in range(len(accessories)):
        if accessories[j]['maxEnhance'] != 5 or accessories[j]['grade'] != 3 or "Manos" in accessories[j]['name']:
            continue
        curr = 0
        for i in range(trials):
            curr += simulate_enhancement(accessories[j], start, stop, rate)
        print(f"Average profit for {accessories[j]['name']}: {curr/trials:,.2f}")
    
    
if __name__ in {"__main__", "__mp_main__"}:
    main()
