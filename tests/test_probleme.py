#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Tests pour la classe Probleme du module prog_dual.
"""
import pytest
from prog_dual import Probleme, Lot, Mon_exception, Mon_exception_lot

@pytest.fixture
def lots():
    """7 lots pour les tests suivants."""
    a = Lot(nom="Lot1", cout=5, type_arme=["caillou", "ciseau"], quantite = [10,1])
    b = Lot(nom="Lot2", cout=2, type_arme=["caillou", "ciseau"], quantite = [7,2])
    c = Lot(nom="Lot3", cout=14, type_arme=["caillou", "lame"], quantite = [15, 7])
    d = Lot(nom="Lot4", cout=20, type_arme=["baton", "lame"], quantite = [7, 6])
    e = Lot(nom="Lot5", cout=20, type_arme=["caillou", "lame", "cuillere"], quantite = [20, 6, 5])
    f = Lot(nom="Lot9", cout=20, type_arme=["caillou", "lame", "cuillere"], quantite = [20, 6, 5])
    g = Lot(nom="Lot9", cout=25, type_arme=["caillou", "lame", "cuillere"], quantite = [18, 6, 5])
    return [a, b, c, d, e, f, g]

def test_verif_liste_arme():
    """verifie que chaque type d'arme est présent une seule fois"""
    with pytest.raises(Mon_exception_lot):
        Lot6 = Lot("Lot6", 20, ["caillou", "lame", "lame"], [20, 6, 5])

def test_verif_cout_quantite_positif():
    """Le cout doit être positive."""
    with pytest.raises(Mon_exception_lot):
        Lot8 = Lot("Lot8", -20, ["caillou", "lame", "cutter"], [20, 6, 5])
        
def test_verif_quantite_arme():
    """autant de types d'armes que de quantite."""
    with pytest.raises(Mon_exception_lot):
        Lot7 = Lot("Lot7", 20, ["caillou", "lame", "cutter"], [20, 6, 5, 7])
        
def test_instanciation(lots):
    """Création."""
    a, b, c, d, e, f, g = lots
    probleme = Probleme(lots=[a,b], demande = [60,10])
    assert isinstance(probleme, Probleme)
    
def test_verif_same_type_arme(lots):
    """vérifie que les lots sont composés du même type d'armes"""
    a, b, c, d, e, f, g = lots
    with pytest.raises(Mon_exception):
        probleme = Probleme([c, d],[60,10])
        
def test_verif_lots_meme_taille(lots):
    """vérifie que les lots ont la même longueur."""
    a, b, c, d, e, f, g = lots
    with pytest.raises(Mon_exception):
        probleme = Probleme([c, e],[60,10])

def test_verif_lots_differents(lots):
    """vérifie que deux lots n'ont pas les mêmes quantités pour tous les types d'armes"""
    a, b, c, d, e, f, g = lots
    with pytest.raises(Mon_exception):
        probleme = Probleme([e, f],[60,10])

def test_verif_noms(lots):
    """vérifie que que deux lots n'ont pas le même nom."""
    a, b, c, d, e, f, g = lots
    with pytest.raises(Mon_exception):
        probleme = Probleme([f, g],[60,10])

def test_verif_deux_lots_min(lots):
    """vérifie que le pb est composé d'au moins deux lot"""
    a, b, c, d, e, f, g = lots
    with pytest.raises(Mon_exception):
        probleme = Probleme([a],[60,10])

def test_verif_lenDemand_len_arme(lots):
    """vérifie que la longueur de liste demande = nb de type d'arme."""
    a, b, c, d, e, f, g = lots
    with pytest.raises(Mon_exception):
        probleme = Probleme([a, b],[60,10,30])
        
def test_lots(lots):
    """Teste la propriété lots."""
    a, b, c, d, e, f, g = lots
    probleme = Probleme([a, b],[60,10])
    assert [a,b]== list(probleme.lots)

def test_noms(lots):
    """Teste la propriété noms."""
    a, b, c, d, e, f, g = lots
    probleme = Probleme([a, b],[60,10])
    assert ["Lot1","Lot2"] == [lot.nom for lot in probleme.lots]


def test_acces(lots):
    """Utilisation de []."""
    a, b, c, d, e, f, g = lots
    probleme = Probleme([a, b],[60,10])
    assert probleme.lots[0] == a


def test_egalite(lots):
    """Doit être différent de l'identité."""
    a, b, c, d, e, f, g = lots
    probleme1 = Probleme([a, b],[60,10])
    probleme2 = Probleme([a, b],[60,10])
    assert probleme1 == probleme2
    
def test_repr():
    """Teste le repr."""
    probleme = Probleme(lots=[Lot(nom='Lot1', cout=5, type_arme=['caillou', 'ciseau'], quantite=[10, 1]), Lot(nom='Lot2', cout=2, type_arme=['caillou', 'ciseau'], quantite=[7, 2])],demande = [60, 10])
    assert (
        repr(probleme) 
        == "probleme(lots=[Lot(nom='Lot1', cout=5, type_arme=['caillou', 'ciseau'], quantite=[10, 1]), Lot(nom='Lot2', cout=2, type_arme=['caillou', 'ciseau'], quantite=[7, 2])],demande = [60, 10])"
    )


def test_encode():
    """Teste l'encodage d'une ligne."""
    correspondance = {
        "Lot1 / 5 / caillou ciseau / 10 2": Lot(nom="Lot1", cout=5, type_arme=["caillou", "ciseau"], quantite=[10, 2]),
        "Lot2 / 10 / caillou ciseau / 9 4": Lot(nom="Lot2", cout=10, type_arme=["caillou", "ciseau"], quantite=[9, 4])
    }
    for entree, attendu in correspondance.items():
        assert attendu == Probleme._encode(entree)


def test_constructeur(lots):
    """Constructeur alternatif."""
    a, b, c, d, e, f, g = lots
    entree = """
Lot1 / 5 / caillou ciseau / 10 1
Lot2 / 2 / caillou ciseau / 7 2
60 10
"""

    probleme2 = Probleme(lots=[a, b],demande = [60,10])
    probleme = Probleme.par_str(entree)
    assert probleme == probleme2
    

    


    
