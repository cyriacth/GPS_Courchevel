import json
from tkinter.filedialog import askopenfilename

REQUEST = 3
WRITE = True

path_in = askopenfilename(initialdir="./data/")

with open(path_in, "r") as f:
        dico = json.load(f)


if REQUEST == 1: # pour partager aux autres

    for i in range(len(dico["pistes"])):
        for j in range(len(dico["pistes"][i]["coords"])):
            dico["pistes"][i]["coords"][j][0] /= 3600 # width
            dico["pistes"][i]["coords"][j][1] /= 3601 # height

    for i in range(len(dico["noeuds"])):
        dico["noeuds"][i]["x"] /= 3600 # width
        dico["noeuds"][i]["y"] /= 3601 # height


elif REQUEST == 2: # lissage + dup (pistes)

    changements = 1

    while changements > 0:
        pistes = []
        changements = 0
        for i in range(len(dico["pistes"])):
            try:
                nom = dico["pistes"][i]["name"]
                nommage_auto = nom[0] == "p" and int(nom[1:])
                if nommage_auto:
                    dico["pistes"][i]["name"] = "p"+str(i+1)
                else:
                    if nom in pistes:
                        dico["pistes"][i]["name"] = input(f"nouveau nom pour '{nom}' : ")
                        changements += 1
                    else:
                        pistes.append(nom)
            except:
                pass

elif REQUEST == 3: # Précision remontée mecanique et tire-fesses

    for i in range(len(dico["pistes"])):
        if dico["pistes"][i]["couleur"] == "yellow":
            print(f'{dico["pistes"][i]["name"]} : {dico["pistes"][i]["noeud_depart"]} vers {dico["pistes"][i]["noeud_fin"]}')
            color_choice = input("téléphérique(1), télécabine(2), télésièges(3) et téléskis(4) ?\n")
            if color_choice == "1":
                dico["pistes"][i]["couleur"] = "téléphérique"
            elif color_choice == "2":
                dico["pistes"][i]["couleur"] = "télécabine"
            elif color_choice == "3":
                dico["pistes"][i]["couleur"] = "télésièges"
            elif color_choice == "4":
                dico["pistes"][i]["couleur"] = "téléskis"
    print("thx")


if WRITE:
    print("writing")
    path_out = "./data/" + input("save as : ") + ".json"
    with open(path_out, "w") as f:
        json.dump(dico, f, indent=2)