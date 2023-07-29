import os
import functools

class Grid:

    def __init__(self, field, cycle_number, life_symbol, death_symbol):
        """
        :param field: list, list listov, hracia plocha
        :param cycle_number: int cislo cyklu/generacie
        :param life_symbol: str symbol pre zivu bunku
        :param death_symbol: str symbol pre mrtvu bunku.
        """
        self.field = field
        self.cycle_number = cycle_number
        self.life_symbol = life_symbol
        self.death_symbol = death_symbol
        self._cls = True

    def __repr__(self):
        """
        Uprava reprezentacie objektu Grid
        :return: string
        """
        if self._cls:
            os.system('cls')
        return_value = f'\n\t\t\033[93m\033[96mGAME OF LIFE\n\tCycle: {self.cycle_number}\n' \
                       f'\tLIVE CELL: {self.life_symbol}\tDEAD CELL: {self.death_symbol}'
        for row in self.field:
            row_string = '\n\t\033[92m'
            for cell in row:
                if cell.state:
                    row_string += '\033[31m' + self.life_symbol + '\033[0m' if not cell.ebola else '\033[1;37m' + self.life_symbol + '\033[0m'
                else:
                    row_string += '\033[33m' + self.death_symbol + '\033[0m'
            return_value += row_string
        return return_value

    def get_value(self, position):
        """
        Navracia hodnotu na pozicii position
        :param position: pozicia
        :return: hodnota 2d pola field na pozicii position
        """
        row, column = position
        return self.field[row][column]

    def is_position_possible(self, position):
        """
        Metoda kontroluje, ci je mozne danu poziciu obsadit.
        :param position: zadana pozicia (x,y)
        :return: bool
        """
        width, height = len(self.field[0]), len(self.field)
        if 0 <= position[0] < height and 0 <= position[1] < width:
            return True
        return False

    def get_cell_neighbor_positions(self, cell_position):
        """
        Metoda navracia list pozicii susednych buniek pre poziciu bunky cell_position
        :param cell_position: Pozicia bunky (x,y)
        :return: list pozicii susednych buniek
        """
        row, column = cell_position
        neighbors_positions = [(nrow, ncol) for nrow in range(row - 1, row + 2) for ncol in
                               range(column - 1, column + 2)]
        neighbors_positions.remove((row, column))
        neighbors_positions = [position for position in neighbors_positions if
                               self.is_position_possible(position)]

        return neighbors_positions

    def get_number_of_live_dead_neighbors(self, cell_position):
        """
        Metoda navracia dvojicu hodnot - pocet zivych susedov, pocet mrtvych susedov.
        :param cell_position: Pozicia bunky (x,y)
        :return:
        """
        neighbors_positions = self.get_cell_neighbor_positions(cell_position)
        neighbors_states = [self.get_value(cell_position).state for cell_position in neighbors_positions]
        number_of_dead_neighbors = neighbors_states.count(False)
        number_of_live_neighbors = neighbors_states.count(True)
        cell = self.get_value(cell_position)
        neighbors = [self.get_value(cell_position) for cell_position in neighbors_positions]
        live_neighbors = [(neighbor.id, neighbor.ebola) for neighbor in neighbors if neighbor.state]
        unique_values = list(set(live_neighbors))
        cell.stack.extend(unique_values)
        cell.stack = list(set(cell.stack))
        return number_of_live_neighbors, number_of_dead_neighbors

    def get_number_of_live_cells(self):
        flatten_field = self.get_flatten_field()
        return len([cell for cell in flatten_field if cell.state])

    def get_number_of_ebola_cells(self):
        flatten_field = self.get_flatten_field()
        return len([cell for cell in flatten_field if cell.ebola])

    def get_number_of_healthy_cells(self):
        return self.get_number_of_live_cells() - self.get_number_of_ebola_cells()

    def get_flatten_field(self):
        return functools.reduce(lambda x,y: x+y, self.field)

    def get_all_live_cells(self):
        return [self.get_value((x, y)) for x in range(len(self.field)) for y in range(len(self.field[x])) if self.get_value((x, y)).state]

    def get_graph_data(self):
        this_cycle_live_cells = self.get_all_live_cells()
        return {cell.id: cell.stack for cell in this_cycle_live_cells}
