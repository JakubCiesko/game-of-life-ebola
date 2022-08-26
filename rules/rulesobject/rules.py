class Rules():
    def __init__(self, grid, threshold_values):
        """
        :param grid: parameter grid, na ktory sa budu aplikovat pravidla
        :param threshold_values: prahove hodnoty, ktore rozhoduju o tom, ktore pravidlo bude aplikovane.
        """
        self.grid = grid
        self.threshold_values = threshold_values

    def apply_rules(self):
        """
            Metoda apply_rules aplikuje pravidla Game-of-life na objekt triedy Grid, objekt je touto aplikaciou zmeneny.
            Pravidla sa aplikuju postupne na vsetky bunky (cell) obsiahnute v mriezke (grid).
            :param grid: Objekt triedy Grid

        """

        field = self.grid.field
        width, height = len(field[0]), len(field)
        for row in range(height):
            for column in range(width):
                cell = self.grid.get_value((row, column))
                live_neighbor_count, dead_neighbor_count = self.grid.get_number_of_live_dead_neighbors((row, column))
                if cell.state:
                    if cell.ebola:
                        cell.ebola_iteration()
                        neighbor_positions = self.grid.get_cell_neighbor_positions((row, column))
                        if cell.ebola_iteration_counter >= self.threshold_values['ebola-infection']:
                            for neighbor_position in neighbor_positions:
                                neighbor = self.grid.get_value((neighbor_position[0],neighbor_position[1]))
                                if neighbor.state and not neighbor.ebola:
                                    neighbor.set_ebola_state(True)

                    if cell.ebola_iteration_counter >= self.threshold_values['ebola-life']:
                        cell.die()

                    if live_neighbor_count < self.threshold_values['underpopulation']:
                        if not self.threshold_values['ebola']:
                            cell.die()
                        continue
                    elif live_neighbor_count < self.threshold_values['survive']:
                        continue
                    elif live_neighbor_count > self.threshold_values['overpopulation']:
                        if not self.threshold_values['ebola']:
                            cell.die()
                        pass
                else:
                    if live_neighbor_count == self.threshold_values['revive']:
                        if not self.threshold_values['ebola']:
                            cell.change_state()
                        pass
        self.grid.cycle_number += 1
        return

class EndGameTester:
    def __init__(self, grid):
        """
        :param grid: objekt triedy Grid potrebny pre vyhodnotenie End Game Testu.
        """
        self.grid = grid

    def test_change(self, field_copy):
        """
        Metoda monitoruje zmenu hodnoty field objektu triedy Grid.
        Pouziva sa na porovnanie objektu triedy Grid pred a po aplikovani pravidiel Game-of-life pre ukoncenie cyklu.
        Navracia True, ak sa field zmeni, a False, ak sa nezmeni.
        :param field_copy: list
        :return: bool grid-pred-aplikovanim-pravidiel == grid-po-aplikovani pravidiel
        """
        field_values = [[cell.get_state() for cell in row] for row in self.grid.field]
        copied_field_values = [[cell_state for cell_state in row] for row in field_copy]
        condition = field_values != copied_field_values or self.grid.get_number_of_ebola_cells()
        return condition