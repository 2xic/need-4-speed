import os

class Snapshot:
    def __init__(self, name) -> None:
        self.path = os.path.join(
            os.path.dirname(__file__),
            "snapshots",
            name
        )

    def create_or_save(self, results):
        if os.path.isfile(self.path):
            with open(self.path, "r") as file:
                return file.read()
        else:
            with open(self.path, "w") as file:
                file.write(results)
            return results
