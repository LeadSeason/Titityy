import os
import time
import json

with open("todo.json", encoding="utf8" ) as h:
    data = json.load(h)
    for x in data:
        print(data[x])