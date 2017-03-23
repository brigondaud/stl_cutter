#!/usr/bin/env python3

"""
Projet decoupeur Baptiste Rigondaud & Yann Burrer
Definition d'une classe triangle en 3 dimensions.
"""
#pylint: disable=R0903
class Triangle:
    """
    Classe Triangle
    """

    def __init__(self, point1, point2, point3):
        """
        Les points en arguments sont trois triplets composés des composantes x y z,
        il représentent chacun les coordonnées des sommets d'un triangle.
        """
        self.sommets = (point1, point2, point3)

    def __str__(self):
        """
        Retourne une chaine contenant les coordonnees des points du triangle
        """
        #Vecteur des points
        coordonees = ["({}, {}, {})".format(point[0], point[1], point[2])\
        for point in self.sommets]
        return "(" + ", ".join(coordonees) + ")"


    def point_reference(self, hauteur_tranche):
        """
        Retourne le point qui est seul de son cote de plan horizontal defini
        par hauteur
        """
        #on retourne le min ou le max des hauteurs en fonction des deux autres points
        if len([point for point in self.sommets if hauteur(point) == hauteur_tranche]) == 2:
            #S'il y a deux points sur le plan : on retourne celui qui n'y est pas
            for point in self.sommets:
                if point[2] != hauteur_tranche:
                    return point
        else:
            return [min([point for point in self.sommets], key=hauteur),
                    max([point for point in self.sommets], key=hauteur)][
                        len([point for point in self.sommets if hauteur(point) < hauteur_tranche]) == 2
                    ]

    def min_coor(self, coor):
        """
        retourne la plus petite coordonnee d'abscisse si coor vaut 0, ordonne si 1
        et cote si 2
        """
        return min(point[coor] for point in self.sommets)

    def max_coor(self, coor):
        """
        retourne la plus grande coordonnee d'abscisse si coor vaut 0, ordonne si 1
        et cote si 2
        """
        return max(point[coor] for point in self.sommets)

def hauteur(point):
    """
    retourne la hauteur d'un point (selon l'axe z)
    """
    return point[2]
