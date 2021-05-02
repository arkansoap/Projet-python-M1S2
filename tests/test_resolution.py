#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Tests pour le module résolurion du module prog_dual.
"""
import pytest
import numpy as np
import scipy.optimize as so
import pulp as pp
from prog_dual import Probleme, Lot, resolution

@pytest.fixture
def probleme():
    """Crée 1 problème simple avec deux lots."""
    problem = Probleme.par_str(
        """
Lot1 / 5 / caillou ciseau / 10 1
Lot2 / 7 / caillou ciseau / 7 2
60 10
"""
    )
    return problem

def test_resoud_pb_LP(probleme):
    Bt = np.matrix([[10,1],[7,2]])
    A = np.array([5,7])
    Ct = np.array([60,10])
    C = Ct.T
    B = Bt.T
    At = A.T

    sp1 = so.linprog(c=A, A_ub=-B, b_ub=-C, method = "highs")
    sd1 = so.linprog(c=-Ct, A_ub = Bt, b_ub=At, method= "highs")
    
    sp, sd = resolution._resoud_pb_LP(probleme)

    assert all(sp)==all(sp1)
    assert all(sd)==all(sd1)
    
def test_resoud_pulp(probleme):
    problem=probleme
    liste_demande, liste_coeff, liste_coefft, liste_cout, liste_arme, liste_lot = resolution._defList(problem)
    prob, results, obj = resolution._resoud_pulp("Prog_dual", liste_arme, liste_coeff,
                                                 liste_demande, liste_cout, True, False)
    caillou = pp.LpVariable("caillou", 0, None, pp.LpContinuous)
    ciseau = pp.LpVariable("ciseau", 0, None, pp.LpContinuous)
    probT = pp.LpProblem("Prog_dual", pp.LpMaximize)
    probT.setObjective(60*caillou + 10*ciseau)
    probT.addConstraint(10*caillou + ciseau  <= 5)
    probT.addConstraint(7*caillou + 2*ciseau  <= 7)
    probT.solve(pp.PULP_CBC_CMD(msg = 0))
    resultsT = list()
    for var in probT.variables():
        resultsT.append(var.value())
    objT = probT.objective.value()
    
    assert obj == objT
    assert results == resultsT