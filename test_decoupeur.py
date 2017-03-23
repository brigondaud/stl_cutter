#!/usr/bin/env python3
"""
Module de test pour le script decoupeur.py
"""
import sys
from decoupeur import parser_arguments, stocker_triangle, fenetre_svg
from objets.Triangle import Triangle
from objets.Tranche import Tranche

def test_parser():
    """
    Tests sur le parser d'arguments
    """
    parser_arguments([])
    print("")
    parser_arguments(["-h", "--help"])
    print()
    parser_arguments(['-s', 'abc'])
    parser_arguments(['-s', '12'])
    parser_arguments(['-s', '-h'])
    tranches, fichier = parser_arguments(["-s", "20"])
    print(tranches, fichier)
    print("")
    tranches, fichier = parser_arguments(["-s", "20", "Tux_printable.stl"])
    print(tranches, fichier)
    print("")

def test_fenetre_svg():
    """
    test la definition de la fenetre svg
    """
    triangles = []
    tri1 = Triangle([0, 2, 3], [5, 2, 4], [6, 1, 0])
    tri2 = Triangle([4, 2, 3], [2, 6, 4], [6, 100, 0])
    tri3 = Triangle([100, 2, 3], [2, 6, 4], [6, 100, 0])
    triangles.append(tri1)
    triangles.append(tri2)
    triangles.append(tri3)
    return fenetre_svg(triangles)


def test_une_tranche(fichier):
    """
    test de decoupe sur une tranche
    """
    triangles = stocker_triangle(fichier)
    for triangle in triangles:
        print(triangle, end="\n")
    cote_max = max([triangle.max_hauteur() for triangle in triangles])
    cote_min = min([triangle.min_hauteur() for triangle in triangles])
    hauteur = cote_max - cote_min
    print(hauteur)
    tranche = Tranche(hauteur/2)
    tranche.intersection_tranche(triangles)
    print(tranche.segments, end="\n")
    print(len(tranche.segments))
    ab, od = fenetre_svg(triangles)
    tranche.dessine_svg("test.svg", ab, od)

if __name__ == "__main__":
    """
    execution des tests si script execute
    """
    # test_parser()
    # test_une_tranche(sys.argv[1])
    # absi, ordo = test_fenetre_svg()
    # print(absi, ordo)
