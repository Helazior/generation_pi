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
import sys
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
OUT_CERCLE_COLOR = [80, 190, 56] #rose
IN_CERCLE_COLOR = [
    MAX_VALUE_COLOR - OUT_CERCLE_COLOR[0],
    MAX_VALUE_COLOR - OUT_CERCLE_COLOR[1],
    MAX_VALUE_COLOR - OUT_CERCLE_COLOR[2]]#bleu
TEXT_COLOR = [0, 0, 0] #noir
BACKGROUND_COLOR = [MAX_VALUE_COLOR, MAX_VALUE_COLOR, MAX_VALUE_COLOR] #blanc

PROPORTION_PIXEL = 4/1000 #par rapport à l'image
SPACE_DIGIT = 3 #espace entre les chiffres
VALUE_BOLD_TEXT = 13 #pour une police plus grasse (échelle * 10)

GIF_NAME = "pi"
DELAY_GIF = f"{600 / NB_IMAGES}"
Coordinate = namedtuple("Coordinate", ['x', 'y'])

class Image():
    """Les images à generer sont des objets Image()"""
    number = NB_IMAGES
    list_names = list()
    full_ba_ppm = bytearray() #bytearray contenant toute l'image
    bytearray_ppm = bytearray()
    ba_with_pi = bytearray()


    def __init__(self, image_size, nb_points):
        """prend en entrée la taille de l'image et le nombre de points"""
        self.size = image_size
        self.nb_points = nb_points
        self.name = str()
        self.files_names = str()
        #entête ppm
        self.ba_entete_ppm = bytearray(
            f"P6\n{self.size} {self.size} {MAX_VALUE_COLOR}\n".encode())


    def add_pi(self, str_approx_pi, pixel_size):
        """superpose le texte de pi sur l'image"""
        start_pos = Coordinate(
            (self.size -
             len(str_approx_pi) * (TAILLE_CARACTERE[0] + SPACE_DIGIT) * pixel_size) // 2,
            (self.size - TAILLE_CARACTERE[1] * pixel_size) // 2)
        pixel_shift = Dimension(0, 0)
        for num_carac, caractere in enumerate(str_approx_pi):
            #Etape 1 : espace entre les différents chiffres
            #donc décaler le caractère selon sa position.
            space_before = pixel_size * num_carac * (TAILLE_CARACTERE.width + SPACE_DIGIT)
            for coord_pix in DICO_LIST_COORD_CHIFFRES[caractere]:
                #Etape 2 : espacer les pixels pour les grossir après
                pixel_shift = Dimension(
                    (pixel_size - 1) * coord_pix[0],
                    (pixel_size - 1) * coord_pix[1])
                #on agrandit la taille de la police
                for i in range((pixel_size + 1) * VALUE_BOLD_TEXT // 10):
                    for j in range((pixel_size + 1) * VALUE_BOLD_TEXT // 10):
                        #Etape 3 : On remplit les pixels manquant pour agrandir le caractere
                        #Etape 4 : On convertit en 1D pour l'insérer
                        indice_img = 3 * (
                            self.size * (coord_pix[1] + pixel_shift.height + start_pos.y + j)\
                            + coord_pix[0] + pixel_shift.width + start_pos.x + space_before + i)
                        self.ba_with_pi[indice_img] = TEXT_COLOR[0]
                        self.ba_with_pi[indice_img + 1] = TEXT_COLOR[1]
                        self.ba_with_pi[indice_img + 2] = TEXT_COLOR[2]


    def write_ppm(self, num_self, str_approx_pi):
        """Écrit l'self dans un nouveau fichier ppm."""
        self.full_ba_ppm = self.ba_entete_ppm + self.ba_with_pi
        self.name = f"img{num_self}_{str_approx_pi}.ppm"
        with open(self.name, 'wb') as file_self:
            file_self.write(self.full_ba_ppm)
        self.list_names.append(self.name)


    def generate_gif(self):
        """Génère un GIF à partir des 10 selfs créées"""
        print("\nCréation du GIF...")
        subprocess.run(
            ["convert", "-delay", DELAY_GIF, "-loop", "0"] + self.list_names +\
            [f"{GIF_NAME}.gif"], check=True)
        print(f"{GIF_NAME}.gif généré avec succès")


    def create(self, acc_points_in_cercle, remaining_points):
        """Place les points de couleur dans une self ppm (P6)"""
        nb_points_actual_image = 0
        for nb_points_actual_image in range(
                1, self.nb_points // self.number + (remaining_points > 0) + 1):
            point = Point()
            bool_is_in_cercle = point.is_in_cercle()
            acc_points_in_cercle += bool_is_in_cercle
            point.convert_to_indice(self.size)
            pos_point_in_self = 3*(point.coord_x + self.size * point.coord_y)
            if bool_is_in_cercle:
                self.bytearray_ppm[pos_point_in_self] = IN_CERCLE_COLOR[0]
                self.bytearray_ppm[pos_point_in_self + 1] = IN_CERCLE_COLOR[1]
                self.bytearray_ppm[pos_point_in_self + 2] = IN_CERCLE_COLOR[2]
            else:
                self.bytearray_ppm[pos_point_in_self] = OUT_CERCLE_COLOR[0]
                self.bytearray_ppm[pos_point_in_self + 1] = OUT_CERCLE_COLOR[1]
                self.bytearray_ppm[pos_point_in_self + 2] = OUT_CERCLE_COLOR[2]
            remaining_points -= 1

        return acc_points_in_cercle, nb_points_actual_image


    def verif_pi_fits_in(self, nb_chiffres_apres_virgule, pixel_size):
        """vérifie que l'affichage du nombre pi rentre bien dans l'self"""
        #+2 pour l'unité et le point
        taille_texte = ((nb_chiffres_apres_virgule + 2) * (TAILLE_CARACTERE[0] + SPACE_DIGIT) +\
                VALUE_BOLD_TEXT // 10) * pixel_size
        if self.size - taille_texte < 0:
            print(nb_chiffres_max)
            print("\nErreur:")
            print("Trop de chiffres après la virgule pour cette taille d'image")
            print("Essayez avec moins de chiffres après la virgule")
            print("Ou prenez une image plus grande.\n")
            sys.exit(2)


    def delete_files(self):
        """Supprime les anciennes selfs (s'il y en a)"""
        self.files_names = glob.glob('img*.ppm')

        for img in self.files_names:
            try:
                os.remove(img)
            except OSError:
                print("Error: %s : %s" % (img, OSError.strerror))


def convert_format(approx_pi, precision):
    """Convertit (float)approx_pi en une chaîne de bonne longueur avec un '-'."""
    str_approx_pi = f"{approx_pi:.{precision}f}"
    return str_approx_pi.replace('.', '-')


def generate_ppm_file(image, nb_chiffres_apres_virgule, pixel_size):
    """Coeur du programme qui va appeler les différentes fonctions pour faire les images ppm"""
    image.bytearray_ppm = bytearray(BACKGROUND_COLOR) * image.size * image.size
    image.list_names = list() #liste des noms des images, utile si on ne les supprime pas au début

    #on rajoute ces points lors des premières boucles
    remaining_points = image.nb_points % image.number
    acc_points_in_cercle = 0
    nb_points_place = 0
    for num_image in range(image.number):
        #Le gros calcul en O(n):
        acc_points_in_cercle, nb_points_actual_image = image.create(
            acc_points_in_cercle, remaining_points)

        nb_points_place += nb_points_actual_image
        nb_points_actual_image = 0
        print(100 * (num_image + 1) // image.number, "%\r", end='')
        approx_pi = 4 * acc_points_in_cercle / nb_points_place
        str_approx_pi = convert_format(approx_pi, nb_chiffres_apres_virgule)
        #on ne copie pas la référence mais seulement les valeurs
        image.ba_with_pi = bytearray(image.bytearray_ppm)
        image.add_pi(str_approx_pi, pixel_size)

        image.write_ppm(num_image, str_approx_pi)

    image.generate_gif()


def main():
    """Vérifie les entrées, supprime les anciennes image et lance generate_ppm_file"""
    #On vérifie que les arguments sont conformes puis on les récupère dans des variables:
    image_size, nb_points, nb_chiffres_apres_virgule = verif_argv.check(\
                                            ["int image_size 50 10000",\
                                             "int nombre_de_points 1 1000000000",\
                                             "int nb_chiffres_apres_virgule 0 30"])

    pixel_size = int(image_size * PROPORTION_PIXEL)
    if pixel_size == 0:
        pixel_size = 1

    #On crait un objet image
    image = Image(image_size, nb_points)

    image.verif_pi_fits_in(nb_chiffres_apres_virgule, pixel_size)
    image.delete_files()
    print(" 0 %\r", end='')
    generate_ppm_file(image, nb_chiffres_apres_virgule, pixel_size)


if __name__ == "__main__":
    main()
