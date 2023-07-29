from grid.gridobject.grid import Grid
from grid.gridfunctions.gridfn  import generate_game_field
from cell.cellobject.cellobj import Cell
from rules.rulesobject.rules import Rules, EndGameTester
from data_collector.data_collector import DataCollector
from data_collector.data_writer import DataWriter
import uuid


class Game:
    def __init__(self) -> None:
        self._settings = None
        self._rules = None 
        self._tester = None 
        self._condition = None
        self._data_collector = None
        self._data_writer = None
        self.ebola_condition = False
        self._grid = None
        self.finished = False
        self.game_id = str(uuid.uuid4())
    
    def set_settings(self, settings):
        self._settings = settings

    def get_settings(self):
        return self._settings
    
    def set_rules(self, rules):
        self._rules = rules

    def get_rules(self):
        return self._rules
    
    def set_tester(self, tester):
        self._tester = tester

    def get_tester(self):
        return self._tester
    
    def set_data_collector(self, data_collector):
        self._data_collector = data_collector
    
    def get_data_collector(self):
        return self._data_collector
    
    def set_data_writer(self, data_writer):
        self._data_writer = data_writer

    def get_data_writer(self):
        return self._data_writer
    
    def get_grid(self):
        return self._grid
    
    def set_grid(self, grid):
        self._grid = grid 
    
    def create_game(self):
        self.ebola_condition = True 
        game_of_life_settings = self.get_settings()
        width = game_of_life_settings['width']
        height = game_of_life_settings['height']
        initial_amount_of_ebola_cells = game_of_life_settings['threshold_values']['initial-number-of-ebola-cells']
        grid = generate_game_field(width, height, Cell, initial_amount_of_ebola_cells)
        grid = Grid(grid, 1,life_symbol = game_of_life_settings['life_symbol'],
                    death_symbol = game_of_life_settings['death_symbol'])

        # RULES CREATION
        self.set_rules(Rules(grid, game_of_life_settings['threshold_values']))

        # DataCollector
        data_collector = DataCollector(grid)
        self.set_data_collector(data_collector)

        # DataWriter
        # data_writer = DataWriter(game_of_life_settings['file_path'], data_collector)
        # data_writer.write_heading() if self.ebola_condition else data_writer.write_no_ebola_heading()
        # self.set_data_writer(data_writer)

        # CREATION OF CYCLE TESTER CONDITION OBJECT
        self.set_tester(EndGameTester(grid))

        self.set_grid(grid)
        return grid
    
    def start_game(self):
        condition = True
        data_collector = self.get_data_collector()
        # data_writer = self.get_data_writer()
        rules = self.get_rules()
        tester = self.get_tester()
        grid = self.get_grid()

        while condition:
            self.get_data_collector()
            data_collector.update_data()
            # Formatting Data
            #data_string = data_collector.get_formatted_SIR_string() if self.ebola_condition else data_collector.get_formatted_data_string()
            # Writing Data
            # data_writer.write_data(data_string)
            # Preparing for Condition Testing
            grid_field_values_copy = [[cell.get_state() for cell in row] for row in grid.field]
            # Applying rules on grid
            rules.apply_rules()
            # sleep(0.05)
            # Testing condition
            condition = tester.test_change(grid_field_values_copy)
        self.finished = True

        # data_writer.close_file()

    def get_alive_cells_coordinates(self):
        grid = self.get_grid()
        return [cell.__dict__ for cell in grid.get_flatten_field() if cell.get_state()]