class Cell:
    def __init__(self, generator, id):
        self.id = id
        self.generator = generator
        self.borders = []

    def __hash__(self):
        return self.id

    def __str__(self):
        return str(self.generator)