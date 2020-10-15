#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os, sys
from time import time

if __name__ == "__main__":
    tab_temps = []
    if len(sys.argv) < 2:
        print("Trop peu d'arguments", file=sys.stderr)
        sys.exit(1)
    pos = 1
    try:
        sys.argv.index("-n")
        pos += 2
        k = int(sys.argv[2])
        if k < 1:
            k = 1
    except ValueError:
        k = 1
    
    try:
        sys.argv.index("-s")
        pos += 1
        s = True
    except ValueError:
        s = False
    for i in range (k):
        temps_prec = time()
        p = os.fork()
        if p == 0: # fils
            try:
                os.execvp(sys.argv[pos], sys.argv[pos:])
            except FileNotFoundError:
                print("Erreur lors du chargement de %s" % sys.argv[pos], file=sys.stderr)
                sys.exit(1)
        
        #suite du père
        pid, status = os.wait()
        if os.WIFEXITED(status): #le fils est mort
            if os.WEXITSTATUS(status) == 0:#réussi
                if s:
                    print("code sortie de la commande:", status)
            else:
                print("Processus %d terminé: échec (code erreur: %d)" % (p, os.WEXITSTATUS(status)))
        temps = time()-temps_prec
        tab_temps.append(temps)
        print("durée execution:",int(temps),"s")
        print("               :",int(temps*10**6),"microsecondes")
        
    print("temps moyen = ", sum(tab_temps)/len(tab_temps), "s")
    sys.exit(0)


