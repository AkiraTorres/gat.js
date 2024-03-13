class HistoricNotFoundException(Exception):
    def __init__(self, id = None):
        self.id = id
        if self.id != None:
            self.message = f"Historic with id {self.id} was not found"
        else:
            self.message = f"Historic was not found"
        super().__init__(self.message)
        