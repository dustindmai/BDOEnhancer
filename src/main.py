import os
import json
import time
from cmscraper import get_enhanceable_accessories
from enhancement_sim import simulate_enhancement, fs_to_rate
from nicegui import ui
from nicegui.events import ValueChangeEventArguments
def startup():
    file_path = os.path.join('src', 'utils', 'accessories.json')
    current_time = time.time()
    if not os.path.exists(file_path) or current_time - os.path.getmtime(file_path) > 24 * 60 * 60:
        t = time.time()
        print("Accessories data is outdated. Fetching new data...")
        accessories = get_enhanceable_accessories()
        with open(file_path, 'w') as file:
            json.dump(accessories, file)
        print("Accessories data has been updated. Time taken: {time.time() - t:.2f} seconds ")
    else:
        print("Accessories data is up to date.")
    with open(file_path, 'r') as file:
        accessories = json.load(file)
    return accessories

def show(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    ui.notify(f"{name}: {event.value}")

def main():
    accessories = startup()
    ui.label(f"Accessories")
    ui.button('Button', on_click=lambda: ui.notify('Click'))
    ui.run()
    '''
    trials = 0
    for j in range(len(accessories)):
        curr = 0
        for i in range(trials):
            curr += simulate_enhancement(accessories[j], 0, 4, [fs_to_rate(18, 0), fs_to_rate(40, 1), fs_to_rate(44, 2), fs_to_rate(110, 3), fs_to_rate(200, 4)])
        print(f"Average profit for {accessories[j]['name']}: {curr/trials:,.2f}")
    '''
if __name__ in {"__main__", "__mp_main__"}:
    main()
