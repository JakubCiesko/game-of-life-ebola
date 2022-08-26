import time
def final_screen_print(grid):
    """
    Final screen print - Printuje vysledok (pocet cyklov/generacii) a grid po dalsom aplikovani pravidiel (bez zmeny, totozny s poslednym)
    :param grid: Objekt triedy Grid
    """
    grid._cls = False
    grid.cycle_number = grid.cycle_number - 1
    print(f'\n\t\t\033[93m\033[96mTOTAL NUMBER OF CYCLES: {grid.cycle_number}\n')
    time.sleep(2)
    grid.cycle_number = str(grid.cycle_number) + ' (+ 1)'
    print('\tNEXT CYCLE WITHOUT CHANGE:')
    print(grid)