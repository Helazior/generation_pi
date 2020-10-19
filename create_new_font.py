#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Écrit automatiquement le module list_chiffres en fonction
de la police créée.

-Met les coordonées des pixels noir dans une list.
-Fait un dictionnaire "carctères" : liste de coordonnées.
-Formate comme il faut le dictionnaire
-Écrit  le dico à la fin du module "create_new_font".
"""
#Crait la police des chiffres.
#Pour cela on peut écrire notre matrice représentant chaque chiffre.
#Un chiffre fait 6 par 22 (mais modifiable)
#On va convertir ça pour gagner en performances et en mémoire.
#Et surtout pour, plus tard, pouvoir faire une interface pour créer sa police.

TAILLE_CARACTERE = (6, 22)
#à mettre dans un module
#________utile pour créer ma structure de donnée____
#_trop long pour le faire tourner à chaque fois, donc écrit en dur.

def new_matrice():
    '''Crée chaque caractère
    n'est jamais utilisé dans le programme
    uniquement pas moi pour faire mes listes automatiquement.'''

    point = ''
    chiffres = ['' for _ in range(10)]

    point = \
    "      "*19 +\
    " *    "+\
    "***   "+\
    " *    "

    chiffres[0] = \
    " **** " + \
    "**  **" + \
    "*    *"*18+\
    "**  **"+\
    " **** "

    chiffres[1] = \
    "     *"+\
    "     *"+\
    "    **"+\
    "   * *"+\
    "   * *"+\
    "  *  *"+\
    "  *  *"+\
    " *   *"+\
    "     *"*14

    chiffres[2] = \
    " **** "+\
    "*    *"*2+\
    "     *"*7+\
    "   ** "+\
    " **   "+\
    "*     "*9+\
    "******"

    chiffres[3] = \
    " **** "+ \
    "*    *"+ \
    "     *"*8+\
    "  *** " +\
    "     *"*9+\
    "*    *"+\
    " **** "

    chiffres[4] = \
    "   *  "*3+\
    "  *   "*4+\
    " *    "*4+\
    "*    *"*3+\
    "******" +\
    "     *"*6+ \
    "     *"

    chiffres[5] = \
    "******"+\
    "*     "*9+\
    "***** "+\
    "     *"*9+\
    "*    *"+\
    " **** "

    chiffres[6] = \
    " **** "+ \
    "*    *"+ \
    "*     "*9+ \
    "***** " +  \
    "*    *"*9+ \
    " **** "

    chiffres[7] = \
    "******"+\
    "     *"*4+\
    "    * "*4+\
    "   *  "*6+\
    "  *   "*7

    chiffres[8] = \
    " **** "+ \
    "*    *"*9+ \
    " **** " +  \
    "*    *"*10+ \
    " **** "

    chiffres[9] = \
    " **** "+ \
    "*    *"*9+ \
    " *****" +  \
    "     *"*9+ \
    "*    *" +  \
    " **** "
    return point, chiffres

def convert_to_coord(dico_chiffres):
    '''On passe dans un format plus petit et optimisé
    on veut en sortie une liste de coordonés aux pixels noir
    '''
    string_carac = ""
    for caractere in dico_chiffres:
        string_carac = dico_chiffres[caractere]
        dico_chiffres[caractere] = list()
        for indice, value in enumerate(string_carac):
            if value == '*':
                pos = (indice % TAILLE_CARACTERE[0], indice // TAILLE_CARACTERE[0])
                dico_chiffres[caractere].append(pos)

def formate_dico(str_dico):
    '''réécrit le dictionnaire pour qu'il revienne à la ligne tous les 100 caractères maximum'''
    ancien_indice = 0
    str_new_dico = ""
    long_ligne = 0
    for i in enumerate(str_dico):
        long_ligne += 1
        #on a une clé ou on est à plus de 90 caractere
        if (long_ligne > 7 and str_dico[i] == "'" and str_dico[i+2] == "'")\
                or (long_ligne > 90 and str_dico[i - 3] == ")"):
            indice_fin = i
            if str_dico[i - 1] == ' ':
                indice_fin -= 1
            str_new_dico += str_dico[ancien_indice:indice_fin] + "\\\n\t"
            ancien_indice = i
            long_ligne = 4
            if str_dico[i - 3] == ")":
                str_new_dico += "\t"
                long_ligne = 8
            continue

    str_new_dico += str_dico[indice_fin:]
    return str_new_dico



def main():
    '''fonction main()'''
    point, chiffres = new_matrice()
    dico_chiffres = {'-' : point}
    for num in enumerate(chiffres):
        dico_chiffres[f"{num}"] = chiffres[num]
    convert_to_coord(dico_chiffres)

    #on récupère ce qui est avant les données:
    with open("list_chiffres.py", 'r') as fd_chiffres:
        entete_prog = ""
        while True:
            ligne_entete = fd_chiffres.readline()
            #on parcourt jusqu'au bout de l'entête
            if not ligne_entete or ligne_entete[:20] == "TAILLE_CARACTERE = (":
                break
            entete_prog += ligne_entete

    with open("list_chiffres.py", 'w') as new_fd_chiffres:
        new_fd_chiffres.write(entete_prog)
        new_fd_chiffres.write(
            f"TAILLE_CARACTERE = Dimension({TAILLE_CARACTERE[0]},\
            {TAILLE_CARACTERE[1]})\n\n")
        str_dico = f"DICO_LIST_COORD_CHIFFRES = {dico_chiffres}"
        #On formate str_dico pour le couper en plusieurs lignes
        str_dico = formate_dico(str_dico)
        new_fd_chiffres.write(str_dico)
        print("Nouvelle police prête !")


if __name__ == "__main__":
    main()
