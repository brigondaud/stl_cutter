#! /usr/bin/env python3
"""
fichier de test
"""

from Triangle import Triangle
from Tranche import Tranche

def fenetre_svg(liste_de_triangles):
    """
    renvoie les dimensions de la future fenetre svg
    """
    abs_min = min([triangle.min_coor(0) for triangle in liste_de_triangles])
    abs_max = max([triangle.max_coor(0) for triangle in liste_de_triangles])
    ord_min = min([triangle.min_coor(1) for triangle in liste_de_triangles])
    ord_max = max([triangle.max_coor(1) for triangle in liste_de_triangles])
    return abs_max - abs_min, ord_max - ord_min

def test_fonction_intersection_plan():
    """
    test la fonction, sachant que tri1 et tri2 sont en intersections, mais pas tri3.
    Le test doit renvoyer True True False
    """
    tri1 = Triangle((1, 2, 3), (4, 5, 6), (4, 5, 2))
    tri2 = Triangle((5, 2, 3), (4, 8, 6), (2, 5, 2))
    tri3 = Triangle((5, 2, 5), (4, 8, 6), (2, 5, 5))
    tri4 = Triangle((5, 2, 3), (4, 8, 3), (2, 5, 3))
    tranche = Tranche(4)
    print(tranche.intersecte_avec(tri1))
    print(tranche.intersecte_avec(tri2))
    print(tranche.intersecte_avec(tri3))
    print(tranche.intersecte_avec(tri4))

def test_dessin():
    """
    test de la création du fichier svg.
    Doit renvoyer un triangle.
    """
    tranche = Tranche(4)
    tranche.segments.append(((200, 400), (500, 80)))
    tranche.segments.append(((500, 80), (80, 300)))
    tranche.segments.append(((80, 300), (200, 400)))
    tranche.dessine_svg("test1.svg", 1000, 1000)

def test_calcul_intersection():
    """
    Fonction de test sur la formule du caclul d'intersection
    """
    tranche = Tranche(2)
    segment = tranche.calcul_intersection(Triangle((2, 0, 0), (4, 0, 0), (2, 0, 3)))
    print(segment)

def test_point_reference():
    """
    Fonction de test de la methode point de reference
    """
    triangle = Triangle((2, 0, 0), (4, 0, 0), (2, 0, 3))
    print(triangle.point_reference(2))
    triangle = Triangle((2, 1, -1), (4, 3, -1), (2, 5, 8))
    print(triangle.point_reference(-1))

def test_min_max():
    """
    test des coordonnees min et max
    """
    tranche = Tranche(4)
    tranche.segments.append(((-200, 400), (500, 80)))
    tranche.segments.append(((500, 80), (80, -300)))
    tranche.segments.append(((80, 300), (200, 400)))
    # absc, ordo = fenetre_svg()
    tranche.dessine_svg("test.svg", 1500, 1500)

def intersection():
    """
    fonction de test d'intersection sur un tetraedre simple
    """
    #pylint: disable=C0103
    t1 = Triangle((0, 0, 0), (1, 0, 0), (0, 0, 1))
    t2 = Triangle((0, 0, 0), (0, 1, 0), (0, 0, 1))
    t3 = Triangle((1, 0, 0), (0, 0, 1), (0, 1, 0))
    tranche = Tranche(0.5)
    tranche.intersection_tranche([t1, t2, t3])
    print(tranche.segments)
    tranche.dessine_svg("tetraedre.svg", 1000, 1000)

if __name__ == "__main__":
    """
    execution des tests si script execute
    """
    test_fonction_intersection_plan()
    #test_point_reference()
    #test_calcul_intersection()
    # test_dessin()
    # test_min_max()
    # intersection()
