import os
import time
import json

json_data = {"kkd": "ddd"}

with open("todo.json", "r+", encoding='utf8') as f:
    data = json.load(f)
    data.update(json_data)
    f.seek(0)
    json.dump(data, f, ensure_ascii=False)
