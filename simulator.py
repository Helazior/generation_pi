#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Le module Python simulator.py sert à calculer l'approximation de pi
grâce à la méthode de Monte-Carlo.
"""

from random import random
from verif_argv import check
#plus rapide que les namedtuples
class Point():
    """Point sert à calculer l'approximation de pi"""

    def __init__(self):
        """Point pris au hasard dans [-1, 1]² (un carré de longueur 2)."""
        self.coord_x = 2 * (random() - 0.5)
        self.coord_y = 2 * (random() - 0.5)

    def convert_to_indice(self, taille_image):
        """On convertit le point de [-1, 1]² à [0, taille_image]."""
        #utilisé dans approximate_pi
        self.coord_x = int((self.coord_x + 1) * taille_image / 2)
        self.coord_y = int((self.coord_y + 1) * taille_image / 2)

    def is_in_cercle(self):
        """
        Prend en entré un objet de class Point()
        Renvoie 1 si le point est dans le cercle
                0 sinon
        """
        return self.coord_x**2 + self.coord_y**2 <= 1


def main():
    """Mode executable permettant de donner une approximation de pi
    en utilisant un nombre de points donné sur la ligne de commande"""
    #mon module pour vérifier les entrées
    # Vérifie qu'on a un entier dans l'interval en entrée
    nombre_de_points = check(["int nombre_de_points 1 1000000000"])
    acc_points_in_cercle = 0
    for _ in range(nombre_de_points):
        point = Point()
        acc_points_in_cercle += point.is_in_cercle()
    print(4 * acc_points_in_cercle / nombre_de_points)

if __name__ == "__main__":
    main()
