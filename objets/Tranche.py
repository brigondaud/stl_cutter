#!/usr/bin/env python3
"""
Projet decoupeur Baptiste Rigondaud & Yann Burrer
Definition de la classe Tranche.
"""

class Tranche:
    """
    Les tranches sont horizontales, seul le paramètre de hauteur importe.
    """

    def __init__(self, hauteur):
        """
        Une tranche prend en argument la hauteur du plan considere ainsi
        qu'une liste de points qui seront reliees pour tracer un polygone.
        une tranche est initialisee avec une liste vide de points.
        """
        self.hauteur = hauteur
        self.segments = []

    def __str__(self):
        """
        Retourne une chaine contenant la hauteur de la tranche et les
        coordonees des points sur la tranche
        """
        #Contient les points du polygone
        chaine_poly = ", ".join(["({}, {})".format(point[0], point[1])\
         for point in self.segments])
        return str(self.hauteur) + ', ' + chaine_poly

    def intersecte_avec(self, triangle):
        """
        Renvoie True si le triangle de la classe Triangle donne en argument
        est en intersection avec la tranche.
        """
        #Liste des hauteurs du point du triangle
        hauteurs = [triangle.sommets[indice][2] for indice in range(3)]
        #Le point intersecte si le min des hauteurs et sous le plan
        #et si le max des hauteurs et au dessus du plan
        return min(hauteurs) < self.hauteur and max(hauteurs) > self.hauteur


    def dessine_svg(self, nom_fichier, abscisse, ordonnee):
        """
        Cree un fichier svg dans lequel tous les points de la tranche sont relies.
        """
        with open(nom_fichier, 'w') as fichier:
            en_tete = "<svg height=\"{}\" width=\"{}\">\n"
            fichier.write(en_tete.format(ordonnee, abscisse))
            #Epaisseur de trait dynamique en fonction de la taille de l'image
            for segment in self.segments:
                stroke = abscisse/100
                if len(segment) == 2:
                    fichier.write("<line x1=\"{}\" y1=\"{}\" x2=\"{}\" y2=\"{}\""\
                    " style=\"stroke:rgb(255,0,0);stroke-width:{}\" />\n"\
                    .format(segment[0][0], segment[0][1], segment[1][0], segment[1][1], stroke))
            fichier.write("</svg>")

    def iter_intersection(self, triangles):
        """
        Itere sur tous les triangles qui intersectent avec Tranche.
        triangles est un iterable (vecteur)
        """
        for triangle in triangles:
            if self.intersecte_avec(triangle):
                yield triangle

    def intersection_tranche(self, triangles):
        """
        rempli le vecteur de segments avec les points d'intersections entre les triangles
        passes en parametre (on suppose que tous les triangles intersectent avec la
        tranche) et la tranche
        """
        for triangle in triangles:
            segment = self.calcul_intersection(triangle)
            self.segments.append(segment)

    def calcul_intersection(self, triangle):
        """
        retourne un segment de l'intersection entre la tranche et le triangle
        """
        point_ref, segment = triangle.point_reference(self.hauteur), []
        for point in triangle.sommets:
            #si le point est different de celui de difference et que le triangle
            #n'est pas confondu avec le plan
            if point != point_ref:
                rapport = (self.hauteur - point[2])/(point_ref[2] - point[2])
                x_i = rapport*(point_ref[0] - point[0]) + point[0]
                y_i = rapport*(point_ref[1] - point[1]) + point[1]
                segment.append((x_i, y_i))
        return segment

    def points(self):
        """
        itere sur tous les points qui consituent les segments
        """
        for segment in self.segments:
            for point in segment:
                yield point
