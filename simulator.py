#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Le module Python simulator.py sert à calculer l'approximation de pi
grâce à la méthode de Monte-Carlo.
"""

import random
#plus rapide que les namedtuples
class Point():
    """Point sert à calculer l'approximation de pi"""

    def __init__(self):
        """Point pris au hasard dans un carré de longueur 2."""
        self.coord_x = 2 * random.random() - 1
        self.coord_y = 2 * random.random() - 1

    def convert_to_indice(self, taille_image):
        """On convertit le point de [-1, 1] à [0, taille_image]."""
        self.coord_x = int((self.coord_x + 1) * taille_image) // 2
        self.coord_y = int((self.coord_y + 1) * taille_image) // 2

    @staticmethod
    def is_in_cercle(point):
        """
        Prend en entré un point de class Point()
        Renvoie 1 si le point est dans le cercle
                0 sinon
        """
        return point.coord_x**2 + point.coord_y**2 <= 1


def main():
    """Mode executable permettant de donner une approximation de pi
    en utilisant un nombre de points donné sur la ligne de commande"""
    #mon module pour vérifier les entrées
    from verif_argv import check
    # Vérifie qu'on a un entier dans l'interval en entrée
    nombre_de_points = check(["int nombre_de_points 1 1000000000"])
    acc_points_in_cercle = 0
    for _ in range(nombre_de_points):
        acc_points_in_cercle += Point.is_in_cercle(Point())
    print(4 * acc_points_in_cercle / nombre_de_points)

if __name__ == "__main__":
    main()
