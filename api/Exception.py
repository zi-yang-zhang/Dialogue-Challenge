class GeneralException(Exception):
    def __init__(self, error=None):
        self.error = error

    @property
    def get_error(self):
        return self.error
