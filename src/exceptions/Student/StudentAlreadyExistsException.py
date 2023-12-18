class StudentAlreadyExistsException(Exception):
    def __init__(self, cpf):
        self.cpf = cpf
        self.message = f"Student with cpf {self.cpf} already exists in the system."
        super().__init__(self.message)
        