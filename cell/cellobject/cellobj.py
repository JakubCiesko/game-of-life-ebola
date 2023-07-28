class Cell:
    def __init__(self, state, position):
        """
        :param state: bool stav bunky: True - Ziva, False - Mrtva
        :param position: iterable (x,y) - pozicia bunky v hracom poli
        """
        self.state = state
        self.position = position
        self.ebola = False
        self.ebola_iteration_counter = 0
        self.stack = list()
        self.id = id(self)

    def get_state(self):
        """
        Navracia hodnotu state objektu triedy Cell
        :return:  state
        """
        return self.state

    def set_state(self, state_value):
        """
        Funkcia meni hodnotu state objektu triedy Cell na zadanu hodnotu state_value
        :param state_value: Zvolena hodnota, ktora ma byt nastavena
        :return:
        """
        self.state = state_value

    def change_state(self):
        """
        Funkcia meni hodnotu state objektu triedy Cell na jej negaciu:
        :return: True if self.state == False else False
        """
        self.set_state(not self.get_state())

    def ebola_iteration(self):
        if self.state and self.ebola:
            self.ebola_iteration_counter += 1

    def set_ebola_state(self, ebola_state):
        self.ebola = ebola_state

    def change_ebola_state(self):
        self.ebola = not self.ebola

    def reset_ebola_counter(self):
        self.ebola_iteration_counter = 0

    def die(self):
        self.reset_ebola_counter()
        self.set_ebola_state(False)
        self.change_state()
        
        