from grid.gridobject.grid import Grid
from grid.gridfunctions.gridfn  import generate_game_field
from cell.cellobject.cellobj import Cell
from functions.inputfunctions import get_input, replay_input
from functions.displayfunctions import final_screen_print
from rules.rulesobject.rules import Rules, EndGameTester
from data_collector.data_collector import DataCollector
from data_collector.data_writer import DataWriter
from time import sleep

# APP LOOP
game = True
while game:
    # PLAYER'S INPUT - INITIAL STATE SETTINGS
    width, height, time_delay, live_cell_symbol, dead_cell_symbol = get_input()

    # SETTINGS DICT
    game_of_life_settings = {
        'life_symbol': live_cell_symbol,
        'death_symbol': dead_cell_symbol,
        'replay_key': 'x',
        'time_delay': time_delay,
        'file_path': './',
        'threshold_values': {'underpopulation': 2,
                            'survive': 4,
                            'overpopulation': 3,
                            'revive': 3,
                             'ebola': False,
                             'ebola-life': 20,
                             'ebola-infection': 15,
                             'initial-number-of-ebola-cells': 10
                            }
    }

    ebola_condition = game_of_life_settings['threshold_values']['ebola']
    if not ebola_condition:
        game_of_life_settings['threshold_values']['initial-number-of-ebola-cells'] = 0

    # GRID CREATION
    initial_amount_of_ebola_cells = game_of_life_settings['threshold_values']['initial-number-of-ebola-cells']
    grid = generate_game_field(width,height,Cell, initial_amount_of_ebola_cells)
    grid = Grid(grid,1,life_symbol = game_of_life_settings['life_symbol'],
                death_symbol = game_of_life_settings['death_symbol'])

    # RULES CREATION
    rules = Rules(grid,game_of_life_settings['threshold_values'])

    # DataCollector
    data_collector = DataCollector(grid)

    # DataWriter
    data_writer = DataWriter(game_of_life_settings['file_path'], data_collector)
    data_writer.write_heading() if ebola_condition else data_writer.write_no_ebola_heading()

    # CREATION OF CYCLE TESTER CONDITION OBJECT
    tester = EndGameTester(grid)

    # GAME OF LIFE LOOP
    condition = True
    while condition:
        print(grid)
        # Collecting Data
        data_collector.update_data()
        # Formatting Data
        data_string = data_collector.get_formatted_SIR_string() if ebola_condition \
            else data_collector.get_formatted_data_string()
        # Writing Data
        data_writer.write_data(data_string)
        # Preparing for Condition Testing
        grid_field_values_copy = [[cell.get_state() for cell in row] for row in grid.field]
        # Applying rules on grid
        rules.apply_rules()
        sleep(game_of_life_settings['time_delay'])
        # Testing condition
        condition = tester.test_change(grid_field_values_copy)
    data_writer.close_file()

    # FINAL SCREEN & REPLAY OPTION
    final_screen_print(grid)
    game = replay_input(game_of_life_settings['replay_key'])
