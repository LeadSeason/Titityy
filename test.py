import os
import time
import json

with open("todo.json", "r+") as file:
    data = json.load(file)
    data.update({"toinen": "emt"})
    file.seek(0)
    json.dump(data, file, indent=4)
