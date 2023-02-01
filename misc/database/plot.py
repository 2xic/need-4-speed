import json
import matplotlib.pyplot as plt
import os

root = os.path.dirname(__file__)

def join(paths):
    return list(map(lambda x: os.path.join(root, x), paths))

for i in join([
    "output/insert.json",
    "output/select.json",
    "output/select_like_text.json",
    "output/select_greater_than_less_than.json",
    "output/select_join.json",
]):
    with open(i, "r") as file:
        data = json.load(file)
        plt.plot(data['x'], data['firebird'], label='firebird')
        plt.plot(data['x'], data['postgres'], label='postgres')
        plt.title(data['description'])
        plt.legend(loc="upper left")
        plt.savefig(
            (join([f"plots/{data['name']}"]))[0]
        )
        plt.clf()
