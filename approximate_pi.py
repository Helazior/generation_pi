#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Approximation de pi avec la méthode de Monte-Carlo.
Ce programme a pour but de générer un GIF représentant cette simulation.

Le programme reçoit 3 arguments depuis la ligne de commande :
-> la taille de l'image (qui est carrée, donc un seul entier) ;
-> le nombre de point n à utiliser dans la simulation ;
-> le nombre de chiffres après la virgule à utiliser dans l'affichage de la valeur
approximative de π.

Le programme génère 10 images .ppm (p6) puis un GIF.
"""
import os
import glob #pour supprimer les anciennes images
import subprocess
from collections import namedtuple

#Mes modules
from simulator import Point
import verif_argv
from list_chiffres import TAILLE_CARACTERE, DICO_LIST_COORD_CHIFFRES, Dimension

NB_IMAGES = 10
MAX_VALUE_COLOR = 255
#couleur des points hors et dans le cercle

#IN_CERCLE_COLOR = [MAX_VALUE_COLOR, MAX_VALUE_COLOR // 3, MAX_VALUE_COLOR // 4]#orange
#OUT_CERCLE_COLOR = [0, MAX_VALUE_COLOR // 8, MAX_VALUE_COLOR // 16]#vert
#TEXT_COLOR = [0, 0, 0] #noir
#BACKGROUND_COLOR = [MAX_VALUE_COLOR, MAX_VALUE_COLOR, MAX_VALUE_COLOR] #blanc

IN_CERCLE_COLOR = [MAX_VALUE_COLOR, MAX_VALUE_COLOR // 4, 0] #orange
OUT_CERCLE_COLOR = [MAX_VALUE_COLOR // 4, 0, MAX_VALUE_COLOR // 4]#bleu
TEXT_COLOR = [0, 0, 0] #noir
BACKGROUND_COLOR = [MAX_VALUE_COLOR, MAX_VALUE_COLOR, MAX_VALUE_COLOR] #blanc

PROPORTION_PIXEL = 4/1000 #par rapport à l'image
SPACE_DIGIT = 3 #espace entre les chiffres
VALUE_BOLD_TEXT = 13 #pour une police plus grasse (échelle * 10)

GIF_NAME = "pi"
DELAY_GIF = f"{600 / NB_IMAGES}"

Coordinate = namedtuple("Coordinate", ['x', 'y'])

def add_pi_into_img(ba_img_ppm_with_pi, str_approx_pi, taille_image, taille_pixel):
    """superpose le texte de pi sur l'image"""
    start_pos = Coordinate(
        (taille_image -
         len(str_approx_pi) * (TAILLE_CARACTERE[0] + SPACE_DIGIT) * taille_pixel) // 2,
        (taille_image - TAILLE_CARACTERE[1] * taille_pixel) // 2)
    pixel_shift = Dimension(0, 0)
    for num_carac, caractere in enumerate(str_approx_pi):
        #Etape 1 : espace entre les différents chiffres
        #donc décaler le caractère selon sa position.
        space_before = taille_pixel * num_carac * (TAILLE_CARACTERE.width + SPACE_DIGIT)
        for coord_pix in DICO_LIST_COORD_CHIFFRES[caractere]:
            #Etape 2 : espacer les pixels pour les grossir après
            pixel_shift = Dimension(
                (taille_pixel - 1) * coord_pix[0],
                (taille_pixel - 1) * coord_pix[1])
            #on agrandit la taille de la police
            for i in range((taille_pixel + 1) * VALUE_BOLD_TEXT // 10):
                for j in range((taille_pixel + 1) * VALUE_BOLD_TEXT // 10):
                    #Etape 3 : On remplit les pixels manquant pour agrandir le caractere
                    #Etape 4 : On convertit en 1D pour l'insérer
                    indice_img = 3 * (
                        taille_image * (coord_pix[1] + pixel_shift.height + start_pos.y + j)\
                        + coord_pix[0] + pixel_shift.width + start_pos.x + space_before + i)
                    ba_img_ppm_with_pi[indice_img] = TEXT_COLOR[0]
                    ba_img_ppm_with_pi[indice_img + 1] = TEXT_COLOR[1]
                    ba_img_ppm_with_pi[indice_img + 2] = TEXT_COLOR[2]

def write_image(str_image_ppm, num_image, str_approx_pi, list_img_names):
    """Écrit l'image dans un nouveau fichier ppm."""
    img_name = f"img{num_image}_{str_approx_pi}.ppm"
    with open(img_name, 'wb') as file_image:
        file_image.write(str_image_ppm)
    list_img_names.append(img_name)

def convert_format(approx_pi, precision):
    """Convertit (float)approx_pi en une chaîne de bonne longueur avec un '-'."""
    str_approx_pi = f"{approx_pi:.{precision}f}"
    return str_approx_pi.replace('.', '-')

def generate_gif(list_img_names):
    """Génère un GIF à partir des 10 images créées"""
    print("\nCréation du GIF...")
    subprocess.run(
        ["convert", "-delay", DELAY_GIF, "-loop", "0"] + list_img_names + [f"{GIF_NAME}.gif"])
    print(f"{GIF_NAME}.gif généré avec succès")

def computes_an_image(
        bytearray_image_ppm, taille_image, acc_points_in_cercle, nb_points, reste_points):
    """Place les points de couleur dans une image ppm (P6)"""
    nb_points_actual_image = 0
    for nb_points_actual_image in range(1, nb_points // NB_IMAGES + (reste_points > 0) + 1):
        point = Point()
        bool_is_in_cercle = point.is_in_cercle(point)
        acc_points_in_cercle += bool_is_in_cercle
        point.convert_to_indice(taille_image)
        pos_point_in_image = 3*(point.coord_x + taille_image * point.coord_y)
        if bool_is_in_cercle:
            bytearray_image_ppm[pos_point_in_image] = IN_CERCLE_COLOR[0]
            bytearray_image_ppm[pos_point_in_image + 1] = IN_CERCLE_COLOR[1]
            bytearray_image_ppm[pos_point_in_image + 2] = IN_CERCLE_COLOR[2]
        else:
            bytearray_image_ppm[pos_point_in_image] = OUT_CERCLE_COLOR[0]
            bytearray_image_ppm[pos_point_in_image + 1] = OUT_CERCLE_COLOR[1]
            bytearray_image_ppm[pos_point_in_image + 2] = OUT_CERCLE_COLOR[2]
        reste_points -= 1

    return acc_points_in_cercle, nb_points_actual_image

def generate_ppm_file(taille_image, nb_points, nb_chiffres_apres_virgule, taille_pixel):
    """Coeur du programme qui va appeler les différentes fonctions pour faire les images ppm"""
    #entête ppm
    bytearray_entete_ppm = bytearray(
        f"P6\n{taille_image} {taille_image} {MAX_VALUE_COLOR}\n".encode())
    bytearray_image_ppm = bytearray(BACKGROUND_COLOR) * taille_image * taille_image
    list_img_names = list() #liste des noms des images, utile si on ne les supprime pas au début

    reste_points = nb_points % NB_IMAGES#on rajoute ces points lors des premières boucles
    acc_points_in_cercle = 0
    nb_points_place = 0
    for num_image in range(NB_IMAGES):
        #Le gros calcul en O(n):
        acc_points_in_cercle, nb_points_actual_image = computes_an_image(
            bytearray_image_ppm, taille_image, acc_points_in_cercle, nb_points, reste_points)

        nb_points_place += nb_points_actual_image
        nb_points_actual_image = 0
        print(100 * (num_image + 1) // NB_IMAGES, "%\r", end='')
        approx_pi = 4 * acc_points_in_cercle / nb_points_place
        str_approx_pi = convert_format(approx_pi, nb_chiffres_apres_virgule)
        #on ne copie pas la référence mais seulement les valeurs
        ba_img_ppm_with_pi = bytearray(bytearray_image_ppm)
        add_pi_into_img(ba_img_ppm_with_pi, str_approx_pi, taille_image, taille_pixel)

        write_image(
            bytearray_entete_ppm + ba_img_ppm_with_pi, num_image, str_approx_pi, list_img_names)

    generate_gif(list_img_names)

def verif_taille_pi_dans_image(taille_image, nb_chiffres_apres_virgule, taille_pixel):
    """vérifie que l'affichage du nombre pi rentre bien dans l'image"""
    #+2 pour l'unité et le point
    taille_texte = (nb_chiffres_apres_virgule + 2) * (TAILLE_CARACTERE[0] + SPACE_DIGIT) *\
        taille_pixel + taille_pixel * VALUE_BOLD_TEXT // 10
    if taille_image - taille_texte < 0:
        print("\nErreur:")
        print("Trop de chiffres après la virgule pour cette taille d'image")
        print("Essayez avec moins de chiffres après la virgule")
        print("Ou prenez une image plus grande.\n")
        exit(2)

def delete_img():
    """Supprime les anciennes images (s'il y en a)"""
    images = glob.glob('img*.ppm')

    for img in images:
        try:
            os.remove(img)
        except OSError:
            print("Error: %s : %s" % (img, OSError.strerror))


def main():
    """Vérifie les entrées, supprime les anciennes image et lance generate_ppm_file"""
    #On vérifie que les arguments sont conformes puis on les récupère dans des variables:
    taille_image, nb_points, nb_chiffres_apres_virgule = verif_argv.check(\
                                            ["int taille_image 50 10000",\
                                             "int nombre_de_points 1 1000000000",\
                                             "int nb_chiffres_apres_virgule 0 30"])

    taille_pixel = int(taille_image * PROPORTION_PIXEL)
    if taille_pixel == 0:
        taille_pixel = 1
    verif_taille_pi_dans_image(taille_image, nb_chiffres_apres_virgule, taille_pixel)
    delete_img()
    print(" 0 %\r", end='')
    generate_ppm_file(taille_image, nb_points, nb_chiffres_apres_virgule, taille_pixel)

if __name__ == "__main__":
    main()
