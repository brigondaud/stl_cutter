#! /usr/bin/env python3
"""
Projet decoupeur : Baptiste Rigondaud & Yann Burrer
Module principal du projet.
Le script decoupe un modele 3D contenu dans un fichier STL et cree
des tranches au format svg dans le dossier images.
"""
import sys
from struct import unpack
from objets.Triangle import Triangle
from objets.Tranche import Tranche

def parser_arguments(arguments):
    """
    Parser les arguments a l'execution du script.
    Verifie les arguments et retourne un nombre de tranches et le chemin vers
    le fichier stl.
    Prend comme unique parametre un vecteur d'arguments (sys.argv).
    """
    aide = "Utilisation : ./decoupeur.py [-h] [-s] [SLICES] [stl_file]"
    tranches, fichier_stl = 0, ""
    if len(arguments) < 2:
        print(aide)
        sys.exit(1)

    #On manipule un iterateur
    arguments = iter(arguments)
    for argument in arguments:
        #Differents cas possibles pour les arguments
        if argument == "-h" or argument == "--help":
            print(aide)
            sys.exit(1)
        elif argument == "-s":
            #si le nombre de slice est correct
            try:
                slices = int(next(arguments))
                tranches = slices
            except ValueError:
                print("Vous n'avez pas entre en nombre de tranche valide.")
            except StopIteration:
                print("Il manque le nombre de tranche après -s")
                sys.exit(1)
            if tranches < 1:
                print("Veuillez entrer un nombre de tranches valide")
                sys.exit(1)
            else:
                try:
                    fichier_stl = next(arguments)
                except StopIteration:
                    print("il manque un nom de fichier en argument")
                    sys.exit(1)
    return tranches, fichier_stl

def itere_flotant(modele_stl):
    """
    itere sur les octets utiles du fichier, a savoir ceux contenant
    les informations sur les coordonnees
    """
    with open(modele_stl, 'rb') as modele:
        octet = modele.seek(80)
        octet = modele.read(4)
        nombre_triangle = unpack('i', octet)[0]
        octet = 0
        while octet < 50*nombre_triangle:
            if octet%50 >= 12 and octet%50 < 48:
                #On commence au 84e octet,
                modele.seek(octet + 84)
                #On ne s'interesse qu'aux octets des coordonnees, qui sont
                #les octets 12 à 47 de chaque triangle.
                #ceux d'avant etant destines au header
                octet += 4
                coordonnee = unpack('f', modele.read(4))[0]
                yield coordonnee
            elif octet%50 >= 48:
                octet += 2
            else:
                octet += 4

def itere_triplet(iterateur):
    """
    Crée un nouvel iterateur en séparant les elements en triplets.
    Sera utile pour former les triangles qui sont des triplets de triples
    (trois points a trois coordonnees)
    Marche uniquement sur un itérateur ayant un nombre d'éléments
    divisible par 3.
    """
    iterateur = iter(iterateur)
    premier = next(iterateur)
    while premier is not None:
        yield [premier, next(iterateur), next(iterateur)]
        premier = next(iterateur)

def stocker_triangle(modele_stl):
    """
    Retourne un vecteur contenant tous les triangles du fichier modele_stl.
    modele_stl contient le chemin vers le modele en 3D
    """
    triangles = []
    for triangle in itere_triplet(itere_triplet(itere_flotant(modele_stl))):
        triangles.append(Triangle(triangle[0], triangle[1], triangle[2]))
    return triangles

def offset(liste_de_triangles):
    """
    prend en argument une liste de triangle et modifie les coordonnees
    de facon a ce que toutes les coordonnees des abscisses et ordonnees
    soient positives
    """
    abs_min = min([triangle.min_coor(0) for triangle in liste_de_triangles])
    ord_min = min([triangle.min_coor(1) for triangle in liste_de_triangles])
    if abs_min > 0 and ord_min > 0:
        return None
    for triangle in liste_de_triangles:
        for point in triangle.sommets:
            point[0] += abs(abs_min)
            point[1] += abs(ord_min)

def fenetre_svg(liste_de_triangles):
    """
    renvoie les dimensions de la future fenetre svg
    """
    abs_min = min([triangle.min_coor(0) for triangle in liste_de_triangles])
    abs_max = max([triangle.max_coor(0) for triangle in liste_de_triangles])
    ord_min = min([triangle.min_coor(1) for triangle in liste_de_triangles])
    ord_max = max([triangle.max_coor(1) for triangle in liste_de_triangles])
    return (abs_max - abs_min)*1.1, (ord_max - ord_min)*1.1

def max_min_cote(liste_de_triangles):
    """
    retourne la hauteur (distance entre le point le plus haut et le plus bas)
    """
    max_cote = max([triangle.min_coor(2) for triangle in liste_de_triangles])
    min_cote = min([triangle.min_coor(2) for triangle in liste_de_triangles])
    return max_cote, min_cote

def main():
    """
    fonction principale
    """
    nombre_tranches, fichier = parser_arguments(sys.argv)
    triangles = stocker_triangle(fichier)
    offset(triangles)
    max_cote, min_cote = max_min_cote(triangles)
    hauteur = max_cote - min_cote
    abscisse, ordonnee = fenetre_svg(triangles)
    for indice in range(nombre_tranches):
        tranche = Tranche((indice+0.5)*hauteur/nombre_tranches + min_cote)
        #Les triangles intersectes
        intersectes = list(tranche.iter_intersection(triangles))
        tranche.intersection_tranche(intersectes)
        tranche.dessine_svg("image_{}.svg".format(indice), abscisse, ordonnee)

if __name__ == "__main__":
    """
    execution du script decoupeur.py
    """
    main()
