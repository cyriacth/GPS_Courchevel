import pickle
from os import remove
from copy import deepcopy

def printnoeud(dico:dict):
    print("\nNom noeud :",dico["nom"])
    print("Liens :")
    for dest in dico["liens"]:
        print(dest)
    print("\n")

path = "./data-test.pickle"

with open(path, "rb") as f:
    data = pickle.load(f)
data_copy = deepcopy(data)

for dico in data:
    printnoeud(dico)


while (nom_noeud:=input("nom du Noeud à modifier : ")) != "":
    for i in range(len(data)):
        if data[i]["nom"] == nom_noeud:
            printnoeud(data[i])
            if (modif:=input("Modifications possibles : 'nom', 'liens' ou 'delete': ")) == "nom":
                data[i]["nom"] = input("Nouveau nom : ")
            elif modif == "liens":
                if (action:=input("append/delete : ")) == "append":
                    noeud = input("noeud desservi par : ")
                    chemin = input("chemin emprunté : ")
                    nature = input("nature de ce chemin : ")
                    data[i]["liens"].append((noeud, [(nature, chemin)]))
                elif action == "delete":
                    del data[i]["liens"][int(input("index du lien à supprimer : "))]
                    break
            elif modif == "delete":
                print(data[i], "supprimé avec succès")
                del data[i]
                break

print("\nOld\n")
for i in data_copy:
    printnoeud(i)
print("\nNew\n")
for i in data:
    printnoeud(i)

if input("Save changes ? (yes)") == "yes":
    remove(path)
    with open(path, "wb") as f:
        pickle.dump(data, f)
    print("sauvegarde effectuée")

print("end of program")