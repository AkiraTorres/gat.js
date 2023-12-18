class StudentNotFoundException(Exception):
    def __init__(self, cpf):
        self.cpf = cpf
        self.message = f"Student with cpf {self.cpf} was not found"
        super().__init__(self.message)
        