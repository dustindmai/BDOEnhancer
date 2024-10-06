import random
from typing import List

def enhance(chance):
    if chance < 0 or chance > 1:
        raise ValueError("Chance must be between 0 and 1")

    if chance == 0:
        return False
    if chance == 1:
        return True
    chance = int(chance * 10_000_000) # Scale the chance for more precision
    bound = 10_000_000
    return random.randint(1, bound) <= chance

def fs_to_rate(fs, lvl):
    if fs < 0:
        raise ValueError("FS cannot be negative")
    if lvl < 0 or lvl > 4:
        raise ValueError("Level must be between 0 and 4 inclusive")
    # Base rates for base - tet
    # For each fs between 0 and softcap, rate increases by rate/10
    # For each fs above softcap, rate increases by rate/50
    rates = [.25, .1, .075, .025, .005]
    # Softcaps for base - tet
    softcaps=[18, 40, 44, 110, 490]
    
    return rates[lvl] + (fs * (rates[lvl] / 10) if fs <= softcaps[lvl] else softcaps[lvl] * (rates[lvl] / 10) + (fs - softcaps[lvl]) * (rates[lvl] / 50 ))

def simulate_enhancement(accessory: dict, start:int, end:int, rates: List[float]):
    if start < 0 or end > 4 or start >= end:
        raise ValueError("Invalid start and end values")
    prof = 0
    i = start
    while i < end:
        prof -= accessory['prices'][0]
        if enhance(rates[i]):
            prof += accessory['prices'][i+1] - accessory['prices'][i]
            i += 1
        else:
            prof -= accessory['prices'][i]
            i=start
    return prof

