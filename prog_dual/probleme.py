#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Classe Probleme permettant de décrire et représenter les données du problème du programme dual.
"""
from typing import Any, Dict, List, Union, Generator
from dataclasses import dataclass
import numpy as np
import pandas as pd

NomLot = str
CoutLot = float
arme = str
Typ_arme = List[arme]
Quantite = List[int]

@dataclass
class Lot:
    """Représente un lot
    
    Exemple : 
    >>> A  = Lot("Lot1", 20, ["caillou", "lame"], [6, 20])
    >>> A
    Lot(nom='Lot1', cout=20, type_arme=['caillou', 'lame'], quantite=[6, 20])
    
    >>> A._set_cout(12)
    >>> A
    Lot(nom='Lot1', cout=12, type_arme=['caillou', 'lame'], quantite=[6, 20])
    """
    nom: NomLot
    cout: CoutLot
    type_arme: Typ_arme
    quantite : Quantite  

    def __post_init__(self):
        self._lot_valide()        

    def _verif_liste_arme(self):
        """verifie que chaque type d'arme est présent une seule fois"""
        for value in self.type_arme:
            cnt = self.type_arme.count(value)
            if cnt != 1:
                raise Mon_exception_lot(f"{value} est présente plus fois!")
                
    def _verif_quantite_arme(self):
        """verifie que  la longueur liste type_arme = longueur liste quantité"""
        if len(self.type_arme) !=  len(self.quantite):
            raise Mon_exception_lot("Il doit y avoir une quantité par type d'arme!") 
            
    def _verif_cout_quantite_positif(self):
        """verifie que les quantités et prix sont > 0"""
        if self.cout < 0:
            raise Mon_exception_lot("Les couts des lots doivent être positif!")
            
    def _lot_valide(self):
        """ vérifie qu'un lot est valide """
        self._verif_liste_arme()
        self._verif_quantite_arme()
        self._verif_cout_quantite_positif()
        
    def _set_cout(self, coût : float):
        if coût >= 0:
            self.cout = coût
        else :
            raise Mon_exception_lot("Le coût d'un lot doit être positif") 

class Mon_exception_lot(Exception):
    pass
            
class Mon_exception(Exception):
    pass
            
class Probleme:
    """Représente les données du programme dual.
    
    Exemple :
    >>> from prog_dual import Probleme    
    >>> probleme = Probleme(lots = [Lot("Lot1", 5, ["caillou", "lame"], [10, 1]),
    ...                             Lot("Lot2", 7, ["caillou", "lame"], [7, 2])],
    ...                     demande = [60,10])
    >>> probleme
    probleme(lots=[Lot(nom='Lot1', cout=5, type_arme=['caillou', 'lame'], quantite=[10, 1]), Lot(nom='Lot2', cout=7, type_arme=['caillou', 'l
    ame'], quantite=[7, 2])],demande = [60, 10])    
    >>> print(probleme)
    Lot(nom='Lot1', cout=5, type_arme=['caillou', 'lame'], quantite=[10, 1])
    Lot(nom='Lot2', cout=7, type_arme=['caillou', 'lame'], quantite=[7, 2])
    Demande = [60, 10]   
    >>> for lot in probleme.lots:
    ...     print(lot)
    ...
    Lot(nom='Lot1', cout=5, type_arme=['caillou', 'lame'], quantite=[10, 1])
    Lot(nom='Lot2', cout=7, type_arme=['caillou', 'lame'], quantite=[7, 2])    
    >>> print(probleme.demande)
    [60, 10]   
    >>> probleme_bis = Probleme(lots = [Lot("Lot1", 5, ["caillou", "lame"], [10, 1]),
    ...                                 Lot("Lot2", 7, ["caillou", "lame"], [7, 2])],
    ...                     demande = [60,10])
    >>> probleme == probleme_bis
    True   
    >>> probleme2 = Probleme.par_str('''
    ... lotA / 13 / fusil canon pierre / 50 10 2
    ... lotB / 18 / fusil canon pierre / 62 8 4
    ... 100 200 1000''')
    >>> print(probleme2)
    Lot(nom='lotA', cout=13, type_arme=['fusil', 'canon', 'pierre'], quantite=[50, 10, 2])
    Lot(nom='lotB', cout=18, type_arme=['fusil', 'canon', 'pierre'], quantite=[62, 8, 4])
    Demande = [100, 200, 1000]   
    """    
    def __init__(self, lots: List[Lot], demande : List[int] ):
        self.lots = lots
        self.demande = demande
        self._pb_valide()
    
    def __repr__(self) -> str:
        """Renvoie la liste de construction."""
        return f"probleme(lots={list(self.lots) !r},demande = {self.demande})" 

    def __str__(self) -> str:
        """Affiche les lots par ligne et la demande."""
        return "\n".join(repr(lot) for lot in self.lots) + f"\nDemande = {self.demande}"
    
    def __eq__(self, autre: Any) -> bool:
        """Egalite."""
        if type(autre) != type(self):
            return False
        return self.lots == autre.lots and self.demande == autre.demande

    def _verif_same_type_arme(self):
        """vérifie que les lots sont composés du même type d'armes"""
        for lot1 in self.lots:
            for lot2 in self.lots:
                if lot1!= lot2 and lot1.type_arme!= lot2.type_arme:
                    raise Mon_exception("les lots ne sont pas composés du même type d'armes")
                    
    def _verif_lots_meme_taille(self):
        """vérifie que les lots ont la même longueur."""
        for lot1 in self.lots:
            for lot2 in self.lots:
                if len(lot1.type_arme) != len(lot2.type_arme) :
                    raise Mon_exception("les lots ne sont pas de même taille!")
                    
    def _verif_lots_differents(self):
        """vérifie que deux lots n'ont pas les mêmes quantités pour tous les types d'armes"""
        for lot1 in self.lots:
            for lot2 in self.lots:
                if lot1 != lot2 and lot1.quantite == lot2.quantite :
                    raise Mon_exception("Deux lots sont identiques!")  

    def _verif_noms(self):
        """vérifie que que deux lots n'ont pas le même nom."""
        for lot1 in self.lots:
            for lot2 in self.lots:
                if lot1 != lot2 and lot1.nom == lot2.nom :
                    raise Mon_exception("Deux lots ont le même nom!")
                    
    def _verif_deux_lots_min(self):
        """vérifie que le pb est composé d'au moins deux lot"""
        if len(self.lots)<2:
            raise Mon_exception("Il faut deux lots au minimum!")
            
    def _verif_lenDemand_len_arme(self):
        """vérifie que la longueur de liste demande (si elle existe) = nb de type d'arme."""
        if len(self.demande)!= len(self.lots[0].type_arme):
            raise Mon_exception("il faut une demande par type d'arme!")
                    
    def _pb_valide(self):
        """vérifie que le problème est valide"""
        self._verif_same_type_arme()
        self._verif_lots_meme_taille()
        self._verif_lots_differents()
        self._verif_noms()
        self._verif_deux_lots_min()
        self._verif_lenDemand_len_arme()        

    @staticmethod
    def _encode(ligne) -> Lot:
        """Encode une ligne en tache."""
        nom, cout, type_arme, quantite = ligne.split("/")
        nom_valide = nom.strip()
        cout_valide = cout.strip()
        cout_valide = int(cout_valide)
        type_arme_valide = type_arme.split()
        quantite_valide = quantite.split()
        for i in range(0,len(quantite_valide)):
            quantite_valide[i]= int(quantite_valide[i])
        return Lot(
            nom=nom_valide, cout=cout_valide, type_arme = type_arme_valide, quantite=quantite_valide
        )

    @classmethod
    def par_str(cls, message: str) -> "Probleme":
        """Constructeur alternatif."""
        lots = list()
        liste_ligne = list()
        for ligne in message.strip().splitlines():
            liste_ligne.append(ligne)
        str_demande = liste_ligne.pop()
        for ligne in liste_ligne:
            lots.append(cls._encode(ligne))
        demande = str_demande.split()
        for i in range(0,len(demande)):
            demande[i]= int(demande[i])        
        return cls(lots, demande)
            
    def _def_matrice(self) -> Union[np.matrix, np.ndarray] :
        """définition de la matrice qui servira à générer le tableau du problème"""
        coeff=[]
        for i in range(0,len(self.lots)):
            coeff.append(self.lots[i].quantite)
        cout_lot = []
        cout_lot_affiche = []
        for i in range(0,len(self.lots)):
            cout_lot.append(self.lots[i].cout)
            cout_lot_affiche.append(self.lots[i].cout)
        demande = [self.demande]
        cout_lot_affiche.append("")   
        X = coeff+demande
        Y = [list(x) for x in zip(*X)]
        Z = Y + [cout_lot_affiche]
        Z = np.matrix(Z)
        return Z, coeff, cout_lot, demande