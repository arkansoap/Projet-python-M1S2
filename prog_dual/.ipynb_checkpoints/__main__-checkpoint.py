#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Démonstration du module.
"""

from prog_dual import resolution, Probleme, Mon_exception, affichage

mon_probleme = Probleme.par_str(
    """
Lot1 / 10000000 / Fusils Grenades Chars Mitrailleuses Bazookas / 500 1000 10 100 80
Lot2 / 12000000 / Fusils Grenades Chars Mitrailleuses Bazookas / 300 2000 20 80 120
Lot3 / 15000000 / Fusils Grenades Chars Mitrailleuses Bazookas / 800 1500 15 15 200
100000 200000 100 400 400
"""
)

print(affichage.genere_table(mon_probleme))

affichage.affichage_solutions(mon_probleme, False)
