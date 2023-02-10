from .timer import timer, times
from .Testcase import Testcase
from .Capsule import Capsule

class StringPeek:
    def __init__(self):
        pass

    @timer
    def list_join(self, capsule):
        return "".join(list(capsule.input)[capsule.index:capsule.index+capsule.step])
    
    @timer
    def string_join(self, capsule):
        str = ""
        for i in range(capsule.index, capsule.index + capsule.step):
            str += capsule.input[i]
        return str

    @timer
    def str_slicing(self, capsule):
        return capsule.input[capsule.index:capsule.index+capsule.step]

if __name__ == "__main__":
    items = StringPeek()
    testcase = Testcase()
    testcase.methods.append(
        items.list_join
    )
    testcase.methods.append(
        items.str_slicing
    )
    testcase.execute(
        Capsule(
            input="test string" * 10_00,
            index=5,
            step=2,
        ),
        validator=items.string_join,
    )
    print(times)
