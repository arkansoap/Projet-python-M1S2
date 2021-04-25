#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Tests pour la classe Probleme du module prog_dual.
"""
import pytest
import numpy as np
import pandas as pd
from prog_dual import resolution, Probleme, Lot

@pytest.fixture
def probleme():
    """Crée 1 problème simple avec deux lots."""
    probleme = Probleme.par_str(
        """
Lot1 / 5 / caillou ciseau / 10 1
Lot2 / 7 / caillou ciseau / 7 2
60 10
"""
    )
    return probleme

@pytest.fixture
def dataframe():
    """Crée 2 dataframe des solutions du probleme ci dessus pour les tests"""
    nomcol = ["Nb de lots"]
    nomrow = ["Lot1", "Lot2"]
    data = np.array([4.0,3.0])
    df_test = pd.DataFrame(data= data, index =  nomrow, columns = nomcol) 
    
    nomcol2 = ["Prix unitaire"]
    nomrow2 = ["caillou", "ciseau"]
    data2 = np.array([0.23,2.69])
    df2_test = pd.DataFrame(data= data2, index =  nomrow2, columns = nomcol2)
    
    return df_test, df2_test

def test_tables_solutions(probleme, dataframe):
    """Vérifie que la fonction tables_solutions génère le bon dataframe"""
    df_test, df2_test = dataframe
    df = resolution.tables_solutions(probleme, "primal", "pulp")
    assert df.columns.all() == df_test.columns.all()
    assert df.index.all() == df_test.index.all()
    assert df.values.all() == df_test.values.all()
    assert df.size == df_test.size

def test_affichage_solutions(probleme, dataframe):
    """Vérifie que l'affichage des solutions est correct"""
    df_test, df2_test = dataframe
    sortie_test =  print(f"Composition de lots optimale pour l'acheteur : \n  {df_test} \n Prix unitaires optimaux pour l'entrant : \n {df2_test}")
    sortie = resolution.affichage_solutions(probleme, "pulp")    
    assert sortie == sortie_test

def test_resume_pulp(probleme):
    prob, res, obj = resolution.resume_pulp(probleme, "dual")
    liste_res = []
    for i in res:
        liste_res.append(round(i,2))
    assert liste_res == [0.23,2.69]
    assert round(obj,0) == 41




