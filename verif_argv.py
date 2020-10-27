#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module qui vérifie et retourne les arguments d'entrés d'un  programme.
Utilisation: check( ["type[ name][ min max]", "type[ name][ min max]",...] )
où type peut-être: "all", "file", "dir", "int", "float",
"str", "bool", "list", "tuple", "dict")
[name] est optionnel
[min max] sont disponibles pour les int et les float

- print un message d'erreur en cas de non castabilité (sans perte) du type,
puis print le message d'utilisation et s'arrête.
- Dans le cas contraire, le programme ne fait rien.
"""

import sys
import os
from collections import namedtuple
Parametre = namedtuple("Parametre", ["type", "name", "min", "max"])

#A FAIRE: (mettre TO DO enlève des points pylint)
#4 rajouter les arguments optionnels
#5/liste de int, de char etc.
#6 mettre un mode non verbeux
#7 demander que le fichier soit lisible etc.
#8 pouvoir mettre uniquement un min et non 'min max'

def utilisation(tab_argv):
    """indique comment utiliser le programme"""
    print("\nUtilisation:", sys.argv[0], end=' ')
    for num_arg in range(len(tab_argv.type)):
        print("(", tab_argv.type[num_arg], ")", tab_argv.name[num_arg], sep='', end=' ')
    print()
    sys.exit(1)

def split_argv(tab_argv):
    """prend une list de ["type[ name][ min max ]", "type[ name][ min max ]",...] et la split en
    une liste de type et une liste de name. name est remplacé par "" lorsqu'il
    n'est pas donné. De même pour min et max"""
    tab_type_argv = list()
    tab_name_argv = list()
    tab_min_argv = list()
    tab_max_argv = list()
    for argv in tab_argv:
        try:
            arg = argv.split()
        except AttributeError:
            arg = [None, None]#est traité dans la suite du code
        tab_type_argv.append(arg[0])
        try:
            tab_name_argv.append(arg[1])
        except IndexError:
            tab_name_argv.append("") #si on ne précise pas le nom
        else:
            #si on a un deuxième argument, on peut rajouter un min et un max
            try:
                tab_min_argv.append(arg[2])
                tab_max_argv.append(arg[3])
            except IndexError:
                tab_min_argv.append("")
                tab_max_argv.append("")


    return Parametre(tab_type_argv, tab_name_argv, tab_min_argv, tab_max_argv)

def check_inter(argument_value, min_value, max_value, tab_argv, num_arg):
    """Vérifie que le nombre est bien dans l'interval."""
    try:
        assert min_value <= argument_value <= max_value #!propre à python, sinon mettre un and
    except AssertionError:
        print("\nErreur : on veut: ", min_value, " ⩽ ", tab_argv.name[num_arg], " ⩽ ",\
        max_value, "\net ", tab_argv.name[num_arg], " = ", argument_value, sep='')
        utilisation(tab_argv)

def file_or_dir(tab_argv, tab_argv_valides, type_argv, argument):
    """Vérifie que le dossier ou fichier existe bien."""
    if type_argv == "file":
        if not os.path.isfile(argument):
            print("L'argument", argument, "doit être un fichier existant.")
            utilisation(tab_argv)
        tab_argv_valides.append(argument)
    elif type_argv is dir:
        if not os.path.isdir(argument):
            print("L'argument", argument, "doit être un dossier existant.")
            utilisation(tab_argv)
        tab_argv_valides.append(argument)


def check(tab_argv):
    """fonction principale à appeler pour vérifier les entrées
    check le nombre d'arguments, et les types et les conditions"""

    tab_argv_valides = list()
    dic_str_to_type = {"all": all, "file": "file", "dir": dir, "int": int, "float": float,\
                     "str": str, "bool": bool, "list": list, "tuple": tuple, "dict": dict}

    nb_valide_arg = len(tab_argv)
    nb_arg_entre = len(sys.argv) - 1

    tab_argv = split_argv(tab_argv)
    try:
        if nb_arg_entre == 1 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
            utilisation(tab_argv)
        assert len(sys.argv) - 1 == nb_valide_arg
        for num_arg in range(nb_valide_arg):
            #on verifie que le programmeur a bien demandé un type qui existe:
            type_argv = dic_str_to_type[tab_argv.type[num_arg]] #peut lèver KeyError
            argument = sys.argv[num_arg + 1]
            #cas particulier:
            if type_argv in ["file", dir]:
                file_or_dir(tab_argv, tab_argv_valides, type_argv, argument)
                continue

            #on convertit la chaine "argument" avec le type voulu,
            #cela va lever l'exception "ValueError" si ce n'est pas possible
            #Avantage: puissant et court
            #Désavantage: peut laisser passer trop de choses
            argument_value = type_argv(argument) #peut lever ValueError

            if type_argv in [int, float] and tab_argv.min[num_arg] != "":
                min_value = type_argv(tab_argv.min[num_arg])
                max_value = type_argv(tab_argv.max[num_arg])
                #fonction pour ne pas avoir plus de 12 branches pour faire plaisir à pylint
                check_inter(argument_value, min_value, max_value, tab_argv, num_arg)

            tab_argv_valides.append(argument_value)


    except AssertionError:
        print(f"AssertionError : Il faut {nb_valide_arg} paramètre(s) et non {len(sys.argv) - 1}.")
        utilisation(tab_argv)

    except ValueError:
        if tab_argv.name[num_arg]:
            print("\nValueError : l'argument numéro ", num_arg + 1, " \"", tab_argv.name[num_arg]\
                  , "\" doit-être un ", tab_argv.type[num_arg], sep='')
        else:
            print("\nValueError : l'argument numéro", num_arg + 1, \
                  "doit-être un", tab_argv.type[num_arg])
        utilisation(tab_argv)

    except KeyError:
        print("\nErreur utilisation dans le programme: type inconnu. types accepté:\
            \n'all', 'file', 'dir', 'int', 'float', 'str', 'bool', 'list', 'tuple', 'dict'")
        sys.exit(2)

    #except PermissionError:
    #    print("Vous n'avez pas les permissions d'écrire")

    if len(tab_argv_valides) == 1:
        return tab_argv_valides[0]

    return tab_argv_valides
