import json

with open("./data/data7.json", "r") as f:
    dico = json.load(f)

for i in range(len(dico["pistes"])):
    dico["pistes"][i]["x"] /= 3600 # width
    dico["pistes"][i]["y"] /= 3601 # height

with open("./data/data7_copy.json", "r") as f:
    json.dump(dico, f)
