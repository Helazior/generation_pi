#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reçoit 3 arguments depuis la ligne de commande :
-> la taille de l'image (qui est carrée, donc un seul entier) ;
-> le nombre de point n à utiliser dans la simulation ;
-> le nombre de chiffres après la virgule à utiliser dans l'affichage de la valeur approximative de π.
"""
import simulator
import verif_argv
import list_chiffres

NB_IMAGES = 10
MAX_VALUE_COLOR = 1
IN_COLOR = [0, 0, MAX_VALUE_COLOR]#bleu
OUT_COLOR = [MAX_VALUE_COLOR, 0, MAX_VALUE_COLOR]#rose
TEXT_COLOR = [0, 0, 0] #noir
BACKGROUND_COLOR = [MAX_VALUE_COLOR, MAX_VALUE_COLOR, MAX_VALUE_COLOR] #white

def add_pi_into_img(str_approx_pi):
    pass

def write_image(str_image_ppm, num_image, str_approx_pi, precision):
    with open(f"img{num_image}_{str_approx_pi}.ppm", 'wb') as file_image:
        file_image.write(str_image_ppm)

def convert_format(approx_pi, precision):
    str_approx_pi = f"{approx_pi:.{precision}f}"
    return str_approx_pi.replace('.', '-')

def generate_ppm_file(taille_image, nb_points, nb_chiffres_apres_virgule):
    #initialisation
    #entête ppm
    print(" 0 %", end='')
    bytearray_entete_ppm = bytearray(f"P6\n{taille_image} {taille_image} {MAX_VALUE_COLOR}\n".encode())
    bytearray_image_ppm = bytearray(BACKGROUND_COLOR) * taille_image * taille_image
    reste_points = nb_points % NB_IMAGES#on rajoute ces points lors des première boucle
    acc_points_in_cercle = 0
    nb_points_place = 0
    for num_image in range(NB_IMAGES):
        for nb_points_actual_image in range(1, nb_points // NB_IMAGES + (reste_points > 0) + 1):
            point = simulator.make_random_point()
            bool_is_in_cercle = simulator.is_in_cercle(point)
            acc_points_in_cercle += bool_is_in_cercle
            point.convert_to_indice(taille_image)
            if bool_is_in_cercle:
                bytearray_image_ppm[3*(point.x + taille_image * point.y)] = IN_COLOR[0]
                bytearray_image_ppm[3*(point.x + taille_image * point.y) + 1] = IN_COLOR[1]
            else:
                bytearray_image_ppm[3*(point.x + taille_image * point.y) + 1] = OUT_COLOR[1]
            reste_points -= 1
    
        nb_points_place += nb_points_actual_image
        nb_points_actual_image = 0
        print("\r", 10 * (num_image + 1), "%", end='')
        approx_pi = 4 * acc_points_in_cercle / nb_points_place
        str_approx_pi = convert_format(approx_pi, nb_chiffres_apres_virgule)
        write_image(bytearray_entete_ppm + bytearray_image_ppm, num_image, str_approx_pi, nb_chiffres_apres_virgule)
    print("\n",approx_pi)

def main():
    """main()"""
    #On vérifie que les arguments sont conformes puis on les récupère dans des variables:
    taille_image, nb_points, nb_chiffres_apres_virgule = verif_argv.check(["int taille_image 10 10000",\
                                                                           "int nombre_de_points 1 10000000",\
                                                                           "int nb_chiffres_apres_virgule 0 20"])

    generate_ppm_file(taille_image, nb_points, nb_chiffres_apres_virgule)

if __name__ == "__main__":
    main()
