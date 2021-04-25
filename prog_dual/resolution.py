
#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Module permettant de résoudre et d'afficher les solutions du problème du programme dual.

- 'frac'  : False pour des lots non fractionnables ou True pour des lots fractionnables
- 'primal'  : True pour les solutions du demandeur ou False pour les solutions de l'entrant

Exemple:

>>> resolution.tables_solutions(probleme, primal = True, frac = False)
      Nb de lots
Lot1         4.0
Lot2         3.0

>>> resolution.affichage_solutions(probleme, frac = False)
Composition de lots optimale pour l'acheteur :
        Nb de lots
Lot1         4.0
Lot2         3.0
 Prix unitaires optimaux pour l'entrant :
          Prix unitaire
caillou           0.23
ciseau            2.69

>>> resolution.resume_pulp(probleme, primal= True)
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
import scipy.optimize as so
import numpy as np
import pandas as pd
from .probleme import Probleme, Lot
import pulp as pp
from typing import Any, Dict, List, Union, Generator

solution = so.optimize.OptimizeResult
coeff = np.ndarray
variable =  pp.LpVariable
prob = pp.LpProblem

######################################################
###### Genere Tableau d'affichage des résultats ######
######################################################

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
        elif primal == False :
            df = _genere_table_dual(probleme, sol_dual.x, True)
    elif frac == False :
        prob, results, obj = resume_pulp(probleme, True)
        probD, resultsD, objD = resume_pulp(probleme, False)
        if primal ==True :
            df = _genere_table_primal(probleme, results)
        elif primal == False :
            df = _genere_table_dual(probleme, resultsD, False)   
    
    return df

def affichage_solutions(probleme: Probleme, frac: bool) -> "Solutions":
    """genere le tableau des solutions des deux programmes (primal et dual)
    - 'frac'  : 'pulp' pour des lots non fractionnables ou 'lp' pour des lots fractionnables
    """
    if frac == True :
        df = tables_solutions(probleme, True, True)
        df2 = tables_solutions(probleme, False, True)
    elif frac == False :
        df = tables_solutions(probleme, True, False) 
        df2 = tables_solutions(probleme, False, False)
    print(f"Composition de lots optimale pour l'acheteur : \n  {df} \n Prix unitaires optimaux pour l'entrant : \n {df2}")

#####################################
###### Résolution avec Linprog ######
#####################################

def _resoud_pb_LP (probleme : Probleme) -> List[solution] :
    """Résoud les programmes primal et dual avec 'linprog', pour des lots fractionnables"""
    Z, B, A, C = probleme._def_matrice()
    A = np.array(A)
    Bt = np.array(B)
    Ct = np.array(C)
    C = Ct.T
    B = Bt.T
    At = A.T
    solution_primal = so.linprog(c=A, A_ub=-B, b_ub=-C , method= "highs")
    solution_dual = so.linprog(c=-Ct, A_ub=Bt, b_ub=At , method= "highs")

    return solution_primal, solution_dual

##################################
###### Résolution avec Pulp ######
##################################

def _defList(probleme : Probleme) -> Union[coeff, variable] :
    """Définit les listes nécessaires pour la résolution avec pulp"""
    liste_demande = probleme.demande
    liste_demande = np.array(liste_demande)
    liste_cout = list()
    for lot in probleme.lots:
        liste_cout.append(lot.cout)
    liste_cout = np.array(liste_cout)
    liste_coeff = list()
    for lot in probleme.lots :
        liste_coeff.append(lot.quantite)
    liste_coeff = np.array(liste_coeff)
    liste_coefft = liste_coeff.T
    armes = probleme.lots[0].type_arme
    liste_arme = list()
    for arme in armes :
        arme = pp.LpVariable(arme, 0, None, pp.LpContinuous)
        liste_arme.append(arme)
    liste_lot = list()
    for lot in probleme.lots :
        lot = pp.LpVariable(lot.nom, 0, None, pp.LpInteger)
        liste_lot.append(lot)
    
    return liste_demande, liste_coeff, liste_coefft, liste_cout, liste_arme, liste_lot


def _resoud_pulp(nom:str, var:List[variable], coeff:coeff, mb1:coeff, mb2:coeff, maxi:bool, sup:bool)->Union[prob,float]:
    """Résoud les programmes primal et dual avec 'pulp', pour des lots non fractionnables"""
    # création problème
    if maxi == True :
        prob = pp.LpProblem(nom, pp.LpMaximize)
    elif maxi == False :
        prob = pp.LpProblem(nom, pp.LpMinimize)
    # création fonction objectif
    b = 0
    for i, j in zip(mb1, var):
        a = i*j
        b = b + a    
    prob.setObjective(b)
    #création des contraintes
    for k, d in zip(coeff, mb2 ) : 
        b = 0
        for i,j in zip(k, var) :
            a = i*j
            b = b + a
        if sup == False:
            prob.addConstraint(b <= d)
        elif sup == True:
            prob.addConstraint(b >= d)
    # résolution du problème 
    prob.solve(pp.PULP_CBC_CMD(msg = 0))
    # création de l'objet prob, des listes des solutions et de la valeur objectif
    results = list()
    for var in prob.variables():
        results.append(var.value())
    obj = prob.objective.value()
    
    return prob, results, obj

def _creationProbleme():
    pass

def _creationContraintes():
    pass

def _solveProb_creaObj():
    pass

def resume_pulp(probleme: Probleme, primal: bool) -> Union[prob,float]:
    """Résumé du programme : données du pb, solutions, valeur de la fonction objectif"""
    liste_demande, liste_coeff, liste_coefft, liste_cout, liste_arme, liste_lot = _defList(probleme)
    if primal == True :
        prob, results, obj = _resoud_pulp("Prog_primal", liste_lot, liste_coefft, liste_cout, liste_demande, False, True)
    elif primal == False :
        prob, results, obj = _resoud_pulp("Prog_dual", liste_arme, liste_coeff, liste_demande, liste_cout, True, False)
    
    return prob, results, obj




