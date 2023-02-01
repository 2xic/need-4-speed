
class GreaterThan:
    def __init__(self, value) -> None:
        self.value = value

    def sql(self, column):
        return f"{column} > '{self.value}%"
