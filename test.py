import os
import time
import json


def todo_add(title, args):

    data = ""   
    json_data = {}
    for s in args:  
        data += s
        data += " " 
    data = data[:-1]

    json_data.update({title:data})
    
    with open("todo.json",'w', encoding='utf8') as f: 
            #json.dump(data, f, ensure_ascii=False) 
            json.dump(json_data, f, indent=4, ensure_ascii=False)

def main():
    title = input("title")

    data = []        
    while True:
        str1 = input()
        if str1 == "":
            break
        data.append(str1)
    print(title)
    print(data)

    todo_add(title, data)

main()
"""
data = {'test': 'ddl aa d'}
with open("todo.json",'w', encoding='utf8') as f: 
    #json.dump(data, f, ensure_ascii=False) 
    json.dump(data, f, indent=4, ensure_ascii=False)
"""