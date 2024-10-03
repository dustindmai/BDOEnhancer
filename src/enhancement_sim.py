import random
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

