import random
import functools

def generate_game_field(width: int, height: int, obj, number_of_ebola = 5):
    """
    Funkcia generuje 2Dpole objektov (obj). Objekty su iniciovane pomocou pozicie (x,y) a nahodne zvolenej bool hodnoty
    True alebo False: obj(bool, (x,y))
    :param width: int sirka hracieho pola
    :param height: int vyska hracieho pola
    :param obj: objekt, ktory obsadi vsetky pozicie na hracom poli
    :return: list: list listov zaplneny zvolenymi objektami
    """

    values = (True, False)
    game_field = [[obj(random.choice(values), (y,x))  for x in range(width)] for y in range(height)]
    live_cells = [cell for cell in functools.reduce(lambda x,y: x+y, game_field) if cell.state ]
    if len(live_cells) < number_of_ebola:
        number_of_ebola = len(live_cells) - 2 if len(live_cells) > 2 else 1
        if len(live_cells) == 0:
            number_of_ebola = 0
    for cell in random.sample(live_cells, number_of_ebola):
        cell.ebola = True
    return game_field

