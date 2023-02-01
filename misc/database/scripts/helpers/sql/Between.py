
class Between:
    def __init__(self, from_value, to_value) -> None:
        self.from_value = from_value
        self.to_value = to_value

    def sql(self, column):
        return f"({column} > '{self.from_value}' AND {column} < '{self.to_value}')"
