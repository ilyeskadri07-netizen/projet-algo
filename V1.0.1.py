# Créé par tpase, le 19/11/2025 en Python 3.7
from PIL import Image as IMG

### VARIABLES ###

### FONCTIONS ###

def decoupe_image(image : IMG) :
    liste_pixels= []
    taille = image.size
    for y in range(taille[1]) :
        ligne = []
        for x in range(taille[0]) :
            r, g, b = image.getpixel((x, y))
            ligne.append((r+g+b)//3)
        liste_pixels.append(ligne)

    return liste_pixels

def remplacement(liste : list) :
    liste_ASCII ="Ñ@#W$9876543210?!abc;:+=~*-,."
    liste_caractere = []
    for ligne in liste :
        caractere = []
        for pixel in ligne :
            caractere.append(liste_ASCII[pixel // 9])
        liste_caractere.append(caractere)
    return liste_caractere


def outpout(liste_caractere : list) :
    outfile = "outpout.txt"
    sortie = open(outfile, "w")
    for ligne in liste_caractere :
        chaine = ""
        for caractere in ligne :
            chaine += caractere
        sortie.write(chaine + "\n")
    sortie.close()
    print("Résultat dans le fichier %s" %outfile)



### MAIN ###

image_source = IMG.open("OIP.jpg")
decoupe = remplacement(decoupe_image(image_source))
outpout(decoupe)

