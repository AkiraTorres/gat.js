class StudentAlreadyExistsException(Exception):
    def __init__(self, identifier):
        self.identifier = identifier
        if len(identifier) > 4:
            self.message = f"Professor with identifier {self.identifier} already exists in the system."
        else:
            self.message = f"Professor with registration {self.identifier} already exists in the system."
        super().__init__(self.message)
        