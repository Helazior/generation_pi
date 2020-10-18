#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
on crait la police des chiffres.
Pour cela on peut écrire notre matrice représentant chaque chiffre.
Un chiffre fait 6 par 22 (mais modifiable)
On va convertir ça pour gagner en performances et en mémoire.

on va mettre les coordonées des pixels noir dans une list.
On va faire un dictionnaire qui convertie les chiffres en 
une liste du chiffre.

Ce dictionnaire sera écrit dans le module "create_new_font"
"""

TAILLE_CARACTERE = (6, 22)
#à mettre dans un module
#________utile pour créer ma structure de donnée____
#_trop long pour le faire tourner à chaque fois, donc écrit en dur.

def new_matrice(point='', chiffres=['']*10):
    '''n'est jamais utilisé dans le programme
    uniquement pas moi pour faire mes listes'''

    point = \
    "      "*19 +\
    " *    "+\
    "***   "+\
    "***   "

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
    "     *"*16

    chiffres[2] = \
    "***** "+\
    "     *"*10+\
    " **** " + \
    "*     "*10+\
    " *****"

    chiffres[3] = \
    "***** "+ \
    "     *"*9+ \
    " **** " +  \
    "     *"*10+ \
    "***** "

    chiffres[4] = \
    "*    *"+ \
    "*    *"*9+ \
    "******" +  \
    "     *"*10+ \
    "     *"

    chiffres[5] = \
    "******"+ \
    "*     "*9+ \
    "******" +  \
    "     *"*10+ \
    "******"

    chiffres[6] = \
    "******"+ \
    "*     "*9+ \
    "******" +  \
    "*    *"*10+ \
    "******"

    chiffres[7] = \
    "******"+ \
    "     *"*9+ \
    "     *" +  \
    "     *"*10+ \
    "     *"


    chiffres[8] = \
    "******"+ \
    "*    *"*9+ \
    "******" +  \
    "*    *"*10+ \
    "******"

    chiffres[9] = \
    "******"+ \
    "*    *"*9+ \
    "******" +  \
    "     *"*10+ \
    "******"
    return point, chiffres

def convert_to_coord(dico_chiffres):
    '''On passe dans un format plus petit et optimisé
    on veut en sortie une liste de coordonés aux pixels noir
    '''
    string_carac = ""
    for caractere in dico_chiffres:
        string_carac = dico_chiffres[caractere]
        dico_chiffres[caractere] = list()
        for indice in range(len(string_carac)):
            if string_carac[indice] == '*':
                pos = (indice % TAILLE_CARACTERE[0], indice // TAILLE_CARACTERE[0])
                dico_chiffres[caractere].append(pos)

def formate_dico(str_DICO):
    ancien_indice = 0
    str_new_dico = ""
    long_ligne = 0
    for i in range(len(str_DICO)):
        long_ligne += 1
        if (long_ligne > 7 and str_DICO[i] == "'" and str_DICO[i+2] == "'") or\
                (long_ligne > 90 and str_DICO[i - 3] == ")"): #on a une clé ou on est à plus de 90 caractere
            indice_fin = i
            if str_DICO[i - 1] == ' ':
                indice_fin -= 1
            str_new_dico += str_DICO[ancien_indice:indice_fin] + "\\\n\t"
            ancien_indice = i
            long_ligne = 4
            if str_DICO[i - 3] == ")":
                str_new_dico += "\t"
                long_ligne = 8
            continue

    str_new_dico += str_DICO[indice_fin:]
    return str_new_dico



def main():
    point, chiffres = new_matrice()
    dico_chiffres = {'-' : point}
    for num in range(len(chiffres)):
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
        new_fd_chiffres.write(f"TAILLE_CARACTERE = {TAILLE_CARACTERE}\n\n")
        str_DICO = f"DICO_LIST_COORD_CHIFFRES = {dico_chiffres}"
        #On formate str_DICO pour le couper en plusieurs lignes
        str_DICO = formate_dico(str_DICO)
        new_fd_chiffres.write(str_DICO)
        print("Nouvelle police prête !")


if __name__ == "__main__":
    main()