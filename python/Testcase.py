
class Testcase:
    def __init__(self):
        self.methods = []

    def execute(self, input, validator, iterations=10_000):
        for _ in range(iterations):
            for i in self.methods:
                assert i(input) == validator(input)
