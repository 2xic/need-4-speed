import time
from collections import defaultdict

class TimeIt:
    def __init__(self, name) -> None:
        self.name = name
        self.entry = defaultdict(list)

    def __enter__(self):
        return self

    def __call__( self, name ):
        self.current_entry = name
        self.start = time.time_ns()
        return self

    def __exit__(self, *_args):
        self.entry[self.current_entry].append(time.time_ns() - self.start)

    def __str__(self) -> str:
        return f"\n{self.name}\n" + \
                "\n".join([
                    f"{key} : {value} ns ({value / 1e6} ms)" for key, value in list(
                        map(lambda x: [x[0], sum(x[1])], self.entry.items())
                    )
                ])+\
                "\n"

    def __repr__(self) -> str:
        return self.__str__()
