

class Capsule:
    def __init__(self, **kwargs):
        self.args = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
        