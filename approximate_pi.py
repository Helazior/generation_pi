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

def add_pi_into_img(ba_img_ppm_with_pi, str_approx_pi, taille_image, taille_pixel=3):
    """superpose les pi dans l'image"""
    #TODO: changer les tuples en class point
    space_digit = 2#espace entre les chiffres
    start_pos = ((taille_image - len(str_approx_pi) * (list_chiffres.TAILLE_CARACTERE[0] + space_digit) * taille_pixel) // 2,\
                  (taille_image - list_chiffres.TAILLE_CARACTERE[1] * taille_pixel) // 2)
    pixel_shift = [0,0]
    for num_carac, caractere in enumerate(str_approx_pi):
        #Etape 1 : espace entre les différents chiffres
        #donc décaler le caractère selon sa position.
        space_before = taille_pixel * num_carac * (list_chiffres.TAILLE_CARACTERE[0] + space_digit)
        for coord_pix in list_chiffres.DICO_LIST_COORD_CHIFFRES[caractere]:
            #Etape 2 : espacer les pixels pour les grossir après
            pixel_shift[0] = (taille_pixel - 1) * coord_pix[0]
            pixel_shift[1] = (taille_pixel - 1) * coord_pix[1]
            for i in range(taille_pixel): #on agrandit la taille de la police
                for j in range(taille_pixel):
                    #Etape 3 : On remplit les pixels manquant pour agrandir le caractere
                    #Etape 4 : On convertit en 1D pour l'insérer
                    indice = 3 * (taille_image * (coord_pix[1] + pixel_shift[1] + start_pos[1] + j) + coord_pix[0] + pixel_shift[0] + start_pos[0] + space_before + i)
                    ba_img_ppm_with_pi[indice] = 0
                    ba_img_ppm_with_pi[indice + 1] = 0
                    ba_img_ppm_with_pi[indice + 2] = 0
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
        ba_img_ppm_with_pi = bytearray(bytearray_image_ppm) #on ne copie pas l'adresse mais seulement les valeurs
        add_pi_into_img(ba_img_ppm_with_pi, str_approx_pi, taille_image, taille_pixel=4)


        write_image(bytearray_entete_ppm + ba_img_ppm_with_pi, num_image, str_approx_pi, nb_chiffres_apres_virgule)
    print("\n",approx_pi)

def main():
    """main()"""
    #On vérifie que les arguments sont conformes puis on les récupère dans des variables:
    taille_image, nb_points, nb_chiffres_apres_virgule = verif_argv.check(\
                                            ["int taille_image 10 10000",\
                                             "int nombre_de_points 1 10000000",\
                                             "int nb_chiffres_apres_virgule 0 20"])

    generate_ppm_file(taille_image, nb_points, nb_chiffres_apres_virgule)

if __name__ == "__main__":
    main()
