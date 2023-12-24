class SubjectNotFoundException(Exception):
    def __init__(self, id):
        self.id = id
        self.message = f"Subject with id {self.id} was not found"
        super().__init__(self.message)
        