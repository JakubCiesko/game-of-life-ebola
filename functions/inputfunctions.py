def get_input():
    """
    Funkcia ziskava hodnoty premennych width, height, time_delay, live_cell_symbol, dead_cell_symbol z inputu.
    Premenne, ktore ziskava z inputu a nemozu byt typu string, su testovane na validitu inputu pomocou funkcie check_input_validity.
    Funkcia navracia spravne tuple pretypovanych elementov (width, height, time_delay, live_cell_symbol, dead_cell_symbol)
    width = int sirka hracieho pola
    height = int vyska hracieho pola
    time_delay = float cas 1 vykreslenia
    live_cell_symbol = string symbol pre zivu bunku
    dead_cell_symbol = string symbol pre mrtvu bunku
    :return: tuple (width, height, time_delay, live_cell_symbol, dead_cell_symbol)
    """
    width, height, time_delay= '', '', ''
    while not check_input_validity(width, int):
        width = input('Zadaj sirku (cele cislo): ')
    while not check_input_validity(height,int):
        height = input('Zadaj vysku (cele cislo): ')
    while not check_input_validity(time_delay, float):
        time_delay = input('Zadaj dobu vykreslenia v sek.: ')
    live_cell_symbol = input('Zadaj symbol zivej bunky: ')
    dead_cell_symbol = input('Zadaj symbol mrtvej bunky: ')
    return int(width),int(height),float(time_delay),live_cell_symbol,dead_cell_symbol

def replay_input(replay_key):
    """
    Funkcia porovna input hraca s parametrom replay_key (string). V pripade rovnosti navrati True, v pripade nerovnosti False.
    :param replay_key: string
    :return: bool
    """
    return replay_key == input('\n\033[93m\033[96m'
                               f'Pokial chces zacat Game of life znovu, stlac klavesu {replay_key} a potvrd enter.\t\033[0m').lower()

def check_input_validity(input,required_input_type):
    """
    Funkcia vracia:
        True, ak je mozne dany input pretypovat na required_input_type
        False, ak nie je mozne dany input pretypovat na required_input_type
    :param input: input testovany na validitu
    :param required_input_type: potrebny typ inputu
    :return: bool
    """

    try:
        required_input_type(input)
        return True
    except ValueError:
        return False
