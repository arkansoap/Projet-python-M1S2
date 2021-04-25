
#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Module permettant la résolution du problème 

"""
import scipy.optimize as so
import numpy as np
from .probleme import Probleme, Lot
import pulp as pp
from typing import Any, Dict, List, Union, Generator

solution = so.optimize.OptimizeResult
coeff = np.ndarray
variable =  pp.LpVariable
prob = pp.LpProblem

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
    if maxi == True :
        prob = pp.LpProblem(nom, pp.LpMaximize)
    elif maxi == False :
        prob = pp.LpProblem(nom, pp.LpMinimize)
    b = 0
    for i, j in zip(mb1, var):
        a = i*j
        b = b + a    
    prob.setObjective(b)
    for k, d in zip(coeff, mb2 ) : 
        b = 0
        for i,j in zip(k, var) :
            a = i*j
            b = b + a
        if sup == False:
            prob.addConstraint(b <= d)
        elif sup == True:
            prob.addConstraint(b >= d)
    prob.solve(pp.PULP_CBC_CMD(msg = 0))
    results = list()
    for var in prob.variables():
        results.append(var.value())
    obj = prob.objective.value()
    
    return prob, results, obj

def resume_pulp(probleme: Probleme, primal: bool) -> Union[prob,float]:
    """Résumé du programme : données du pb, solutions, valeur de la fonction objectif"""
    liste_demande, liste_coeff, liste_coefft, liste_cout, liste_arme, liste_lot = _defList(probleme)
    if primal == True :
        prob, results, obj = _resoud_pulp("Prog_primal", liste_lot, liste_coefft, liste_cout, liste_demande, False, True)
    elif primal == False :
        prob, results, obj = _resoud_pulp("Prog_dual", liste_arme, liste_coeff, liste_demande, liste_cout, True, False)
    
    return prob, results, obj




