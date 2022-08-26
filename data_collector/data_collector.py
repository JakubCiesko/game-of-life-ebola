class DataCollector:
    def __init__(self,grid):
        self.grid = grid
        self.living_cells = 0
        self.healthy_cells = 0
        self.sick_cells = 0
        self.cycle_number = 0
        self.population = self.grid.get_number_of_live_cells()
        self.last_iteration_living_cells = 0
        self.dead = 0
        self.dead_cummulation = 0

    def update_data(self):
        grid = self.grid
        self.last_iteration_living_cells = self.living_cells
        self.living_cells = grid.get_number_of_live_cells()
        self.dead = self.last_iteration_living_cells - self.living_cells
        self.dead_cummulation += self.dead
        self.healthy_cells = grid.get_number_of_healthy_cells()
        self.sick_cells = grid.get_number_of_ebola_cells()
        self.cycle_number = grid.cycle_number

    def get_data(self):
        return self.living_cells,self.healthy_cells,self.sick_cells

    def get_SIR(self):
        return self.healthy_cells, self.sick_cells, self.population - self.healthy_cells - self.sick_cells

    def get_formatted_SIR_string(self):
        s,i,r = self.get_SIR()
        return f'{self.cycle_number}\t{s}\t{i}\t{r}\t{self.population}\n'

    def get_formatted_data_string(self):
        return f'{self.cycle_number}\t{self.living_cells}\t{self.dead}\t{self.dead_cummulation}\t{self.population}\n'