class DataWriter:
    def __init__(self, file_path, DataCollector):
        self.file_path = file_path
        self.file = open(self.file_path, 'w')
        self.DataCollector = DataCollector
        self.grid = self.DataCollector.grid

    def write_heading(self):
        self.file.write('t\tS\tI\tR\tN\n')

    def write_no_ebola_heading(self):
        self.file.write('t\tactual population: n \ti-th iteration population change: dn\toverall population change: Sum(dn0...dni)\tinitial population No\n')

    def write_data(self, data):
        self.file.write(data)
        if self.grid.cycle_number % 100:
            self.file.close()
            self.file = open(self.file_path, 'a')

    def close_file(self):
        self.file.close()
