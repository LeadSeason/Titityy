import os
import time
import json
arg = input()
k = open(arg)
h = k.read()
k.close()
style = ""
if arg.endswith(".py"):
    style = "py"
if arg.endswith(".json"):
    style = "json"
print("```" + style + "\n" + h + "```")