class SubjectAlreadyExistsException(Exception):
    def __init__(self, id):
        self.id = id
        self.message = f"Subject with id {self.id} already exists in the system."
        super().__init__(self.message)
        