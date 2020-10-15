#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Le module Python simulator.py sert à calculer l'approximation de pi
"""

import random
#plus rapide que les namedtuples
class Point():
    """
    remplace un namedtuples
    """
    def __init__(self, coord_x, coord_y):
        self.x = coord_x
        self.y = coord_y

    def convert_to_indice(self, taille_image):
        self.x = int((self.x + 1) * taille_image) // 2
        self.y = int((self.y + 1) * taille_image) // 2

def make_random_point():
    """
    renvoie un Point aléatoire dans [-1, 1]**2
    """
    return Point(2 * random.random() - 1, 2 * random.random() - 1)

def is_in_cercle(point):
    """
    prend un namedtuples "Point" en entré
    renvoie 1 si le point est dans le cercle
    0 sinon
    """
    return (point.x**2 + point.y**2 <= 1)


def main():
    """Mode executable permettant de donner une approximation de pi
    en utilisant un nombre de points donné sur la ligne de commande"""
    from verif_argv import check
    # Vérifie qu'on a un entier dans l'interval en entré
    nombre_de_points = check(["int nombre_de_points 1 1000000000"])
    acc_points_in_cercle = 0
    for _ in range(nombre_de_points):
        acc_points_in_cercle += is_in_cercle(make_random_point())
    print(4 * acc_points_in_cercle / nombre_de_points)

if __name__ == "__main__":
    main()
