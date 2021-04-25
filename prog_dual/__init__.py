#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description:

Exemple :

>>> from prog_dual import Probleme, Lot, resolution                                                          
>>> mon_probleme = Probleme.par_str('''                                                                      
... Lot1 / 10000000 / Fusils Grenades Chars Mitrailleuses Bazookas / 500 1000 10 100 80                      
... Lot2 / 12000000 / Fusils Grenades Chars Mitrailleuses Bazookas / 300 2000 20 80 120                      
... Lot3 / 15000000 / Fusils Grenades Chars Mitrailleuses Bazookas / 800 1500 15 15 200                      
... 100000 200000 100 400 400                                                                                
... ''') 
>>> mon_probleme.genere_table()
                   Lot1      Lot2      Lot3 demande
Fusils              500       300       800  100000
Grenades           1000      2000      1500  200000
Chars                10        20        15     100
Mitrailleuses       100        80        15     400
Bazookas             80       120       200     400
cout_lot       10000000  12000000  15000000
>>> resolution.affichage_solutions(mon_probleme, "pulp")
Composition de lots optimale pour l'acheteur :
        Nb de lots
Lot1         1.0
Lot2         9.0
Lot3       121.0
 Prix unitaires optimaux pour l'entrant :
                Prix unitaire
Bazookas                0.00
Chars                   0.00
Fusils              10434.78
Grenades             4434.78
Mitrailleuses           0.00 

Remarque:

On pourra faire python -m prog_dual pour un exemple avec des lots non fractionnables.
"""


from .probleme import Probleme, Lot, Mon_exception, Mon_exception_lot
from prog_dual import resolution

__all__ = ["Probleme", "Lot", "Mon_exception", "Mon_exception_lot", "resolution"]