import json

# Charger le JSON depuis un fichier
with open("data\courchevelwithspeed.json") as json_file:
    data = json.load(json_file)

# Accéder à la partie des "pistes" du JSON
pistes = data["pistes"]

# Parcourir chaque piste dans une boucle
for piste in pistes:
    piste["longueur"] = round(piste["longueur"] * 6.097560975609757, 2)
    if piste["couleur"] in ["green", "blue", "red", "black"]:
        piste["temps"] = round(piste["longueur"] / 7, 2)
    elif piste["couleur"] == "t\u00e9l\u00e9skis":
        piste["temps"] = round(piste["longueur"] / 3.8, 2) + 60
    elif piste["couleur"] == "t\u00e9l\u00e9si\u00e8ges":
        piste['temps'] = round(piste["longueur"] / 2.3, 2) + 60
    elif piste["couleur"] == "t\u00e9l\u00e9cabine":
        piste['temps'] = round(piste["longueur"] / 6, 2) + 60
    elif piste["couleur"] == "t\u00e9l\u00e9ph\u00e9rique":
        piste['temps'] = round(piste["longueur"] / 11, 2) + 60


# Enregistrer le JSON mis à jour dans un fichier
with open("data\courchevelwithspeed.json", "w") as json_file:
    json.dump(data, json_file)