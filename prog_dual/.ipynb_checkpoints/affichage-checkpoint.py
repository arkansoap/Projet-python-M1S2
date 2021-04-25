#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Module permettant d'afficher le problème et les solutions du problème du programme dual.

- 'frac'  : False pour des lots non fractionnables ou True pour des lots fractionnables
- 'primal'  : True pour les solutions du demandeur ou False pour les solutions de l'entrant

Exemple:

>>> affichage.tables_solutions(probleme, primal = True, frac = False)
      Nb de lots
Lot1         4.0
Lot2         3.0

>>> affichage.affichage_solutions(probleme, frac = False)
Composition de lots optimale pour l'acheteur :
        Nb de lots
Lot1         4.0
Lot2         3.0
 Prix unitaires optimaux pour l'entrant :
          Prix unitaire
caillou           0.23
ciseau            2.69

>>> affichage.resume_pulp(probleme, primal= True)
(primal:
MINIMIZE
5*Lot1 + 7*Lot2 + 0
SUBJECT TO
_C1: 10 Lot1 + 7 Lot2 >= 60

_C2: Lot1 + 2 Lot2 >= 10

VARIABLES
0 <= Lot1 Integer
0 <= Lot2 Integer
, [4.0, 3.0], 41.0)

"""
import pulp as pp
import numpy as np
import pandas as pd
from typing import Any, Dict, List, Union, Generator
from .probleme import Probleme, Lot
from .resolution import _resoud_pb_LP, _resoud_pulp, _defList

prob = pp.LpProblem
    
def genere_table(probleme : Probleme) -> pd.DataFrame :
    """retourne le tableau des données du problème"""
    nomcol = []
    nomrow =[]
    armes = []
    data = probleme._def_matrice()[0]
    nb_lot = len(probleme.lots)
    armes = probleme.lots[0].type_arme
    nomLot = list()
    for i in range(0, nb_lot):
        lot = (f"{probleme.lots[i].nom}")
        nomLot.append(lot)               
    nomcol = nomLot
    nomcol.append("demande")
    nomrow = armes + ["cout_lot"]          
    df = pd.DataFrame(data= data, index =  nomrow, columns = nomcol)        

    return df

def _genere_table_primal(probleme: Probleme, sol_primal: float) -> pd.DataFrame :
    """genere le tableau des résultats du programme primal"""
    nomcol = []
    nomrow =[]
    data = list()
    for i in sol_primal :
        a = round(i,2)
        data.append(a)
    data = np.array(data)
    data = data.T
    nb_lot = len(probleme.lots)
    nomLot = list()
    for i in range(0, nb_lot):
        lot = (f"{probleme.lots[i].nom}")
        nomLot.append(lot)        
    nomrow = nomLot
    nomcol = ["Nb de lots"]
    df = pd.DataFrame(data= data, index =  nomrow, columns = nomcol) 
    
    return df
    
def _genere_table_dual(probleme: Probleme, sol_dual: float, frac: bool) -> pd.DataFrame :
    """genere le tableau des résultats du programme dual
     - 'frac'  :  True pour des lots fractionnables ou False pour des lots non fractionnables
    """
    nomcol = list()
    nomrow = list()
    armes = list()
    data = list()
    for i in sol_dual:
        a = round(i,2)
        data.append(a)
    data = np.array(data)
    data = data.T
    armes = probleme.lots[0].type_arme        
    nomcol = ["Prix unitaire"]
    if frac == True :
        nomrow = armes
    elif frac == False :
        nomrow = sorted(armes)
    df2 = pd.DataFrame(data= data, index =  nomrow, columns = nomcol)
    
    return  df2

def tables_solutions(probleme: Probleme, primal: bool, frac: bool) -> pd.DataFrame:
    """genere le tableau des solutions en fonctions de paramètres :
    - 'frac'  : False pour des lots non fractionnables ou True pour des lots fractionnables
    - 'primal'  : True pour les solutions du demandeur ou False pour les solutions de l'entrant
    """
    if frac == True:
        sol_primal, sol_dual = _resoud_pb_LP(probleme)
        if primal == True :
            df = _genere_table_primal(probleme, sol_primal.x)
        else:
            df = _genere_table_dual(probleme, sol_dual.x, True)
    else :
        prob, results, obj = resume_pulp(probleme, True)
        probD, resultsD, objD = resume_pulp(probleme, False)
        if primal ==True :
            df = _genere_table_primal(probleme, results)
        else:
            df = _genere_table_dual(probleme, resultsD, False)   
    
    return df

def affichage_solutions(probleme: Probleme, frac: bool) -> "Solutions":
    """genere le tableau des solutions des deux programmes (primal et dual)
    - 'frac'  : 'pulp' pour des lots non fractionnables ou 'lp' pour des lots fractionnables
    """
    if frac == True :
        df = tables_solutions(probleme, True, True)
        df2 = tables_solutions(probleme, False, True)
    else :
        df = tables_solutions(probleme, True, False) 
        df2 = tables_solutions(probleme, False, False)
    print(f"Composition de lots optimale pour l'acheteur : \n  {df} \n Prix unitaires optimaux pour l'entrant : \n {df2}")
    
def resume_pulp(probleme: Probleme, primal: bool) -> Union[prob,float]:
    """Résumé du programme : données du pb, solutions, valeur de la fonction objectif"""
    liste_demande, liste_coeff, liste_coefft, liste_cout, liste_arme, liste_lot = _defList(probleme)
    if primal == True :
        prob, results, obj = _resoud_pulp("Prog_primal", liste_lot, liste_coefft, liste_cout, liste_demande, False, True)
    else :
        prob, results, obj = _resoud_pulp("Prog_dual", liste_arme, liste_coeff, liste_demande, liste_cout, True, False)
    
    return prob, results, obj