class ProfessorNotFoundException(Exception):
    def __init__(self, identifier):
        self.identifier = identifier
        if len(identifier) > 4:
            self.message = f"Professor with cpf {self.identifier} was not found"
        else:
            self.message = f"Professor with registration {self.identifier} was not found"
        super().__init__(self.message)
        