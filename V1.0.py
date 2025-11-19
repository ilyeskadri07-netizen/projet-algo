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
    liste_ASCII ="Ñ@#W$9876543210?!abc;:+=-,._ "
    liste_caractere = []
    for ligne in liste :
        caractere = []
        for pixel in ligne :
            caractere.append(liste_ASCII[pixel // 9])
        liste_caractere.append(caractere)
    return liste_caractere


def affichage(liste_caractere : list) :
    for ligne in liste_caractere :
        chaine = ""
        for caractere in ligne :
            chaine += caractere
        print(chaine)



### MAIN ###

image_source = IMG.open("image.jpg")
decoupe = remplacement(decoupe_image(image_source))
affichage(decoupe)
