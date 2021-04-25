#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Libraire pour un gui de la librairie ordonnancement.
"""
import ipywidgets as ipw
from IPython.display import display
from  prog_dual import Probleme, Lot, Mon_exception, Mon_exception_lot, resolution

red = '\033[91m'
green = '\033[92m'
blue = '\033[94m'
bold = '\033[1m'
italics = '\033[3m'
underline = '\033[4m'
end = '\033[0m'
titre_appli = red + bold + "SOLUTIONS DU PROBLEME DE VENTE D'ARMES" + end
titre_init = green + underline + "Guide pour l'utilisateur :" + end

class Application:
    def __init__(self):
        self.bouton = ipw.Button(description="Résoudre")
        self.bouton2 = ipw.Button(description = "actualiser")
        self.zone_entree = ipw.Textarea(value=
"""Lot1 / 5 / caillou ciseau / 10 1
Lot2 / 7 / caillou ciseau / 7 2
60 10
""", layout=ipw.Layout(height="80px", width = "700px"), description = "données")
        self.probleme = Probleme.par_str(self.zone_entree.value)
        self.zone_probleme = ipw.Output()
        self.zone_solution_primal = ipw.Output()
        self.zone_solution_dual = ipw.Output()
        self.zone_curs_cout = ipw.Output()
        self.zone_titre = ipw.Output()
        self.zone_text_init = ipw.Textarea(value="""'nom_lot' / 'cout_lot' / 'liste_types' / quantite_par_type' -> une ligne par lot
Demande -> une seule ligne 
        
- Un exemple introductif est déjà présent. 
- Attention de respecter le même ordre pour pour les listes type d'arme et quantités
- 'Résoudre' résoud le problème à partir des données rentrées dans le tableau de donnée .
- 'Actualiser' résoud avec les valeurs de coût actualisée par les curseurs.
- Les curseurs s'afficheront automatiquement après la première résolution
- Pour une explication détaillée du contexte du problème, voir les fichiers 'README' et 'rapport'""", layout=ipw.Layout(height="100px", width = "700px"), disabled=True)
        self.zone_titre_init = ipw.Output()
        self.total = ipw.VBox(
            [
                ipw.Box([self.zone_titre], layout = ipw.Layout(justify_content = "center")),
                ipw.VBox([self.zone_titre_init, self.zone_text_init]),
                ipw.VBox([self.bouton, self.zone_entree]),
                ipw.HBox(
                    [
                        self.zone_probleme,
                        self.zone_solution_primal,
                        self.zone_solution_dual
                    ]),
                ipw.HBox([self.zone_curs_cout, self.bouton2]),
            ]
        )
        self.bouton.on_click(self._sur_clique)
        self.bouton2.on_click(self._sur_clique2)
        

        
    def affichage(self):
        with self.zone_titre:
            display(tit = print(titre_appli), align="center")
        with self.zone_titre_init:
            display(tit = print(titre_init))
        display(self.total)
    
    
    def _sur_clique(self, b):
        try:
            self.probleme = Probleme.par_str(self.zone_entree.value)
            self.zone_curs_cout.clear_output()
            self.zone_probleme.clear_output()
            self.zone_solution_primal.clear_output()
            self.zone_solution_dual.clear_output()        
            with self.zone_probleme:
                display(self.probleme.genere_table())
            with self.zone_solution_primal:
                display(resolution.tables_solutions(self.probleme, primal = True, frac = False))
            with self.zone_solution_dual:
                display(resolution.tables_solutions(self.probleme, primal = False, frac = False))
            with self.zone_curs_cout:
                for i in range(0,len(self.probleme.lots)):
                    a = self.probleme.lots[i].cout
                    display(curseur = ipw.interact(self.probleme.lots[i]._set_cout, coût=(0, a*2, round((a/100),1))))
        except Mon_exception:
            with self.zone_probleme:
                self.zone_probleme.clear_output()
                self.zone_solution_primal.clear_output()
                self.zone_solution_dual.clear_output()
                self.zone_curs_cout.clear_output()
                display(erreur= print("Il y a un problème avec les données rentrées. \nLe problème n'est pas valide."))
        except Mon_exception_lot:
            with self.zone_probleme:
                self.zone_probleme.clear_output()
                self.zone_solution_primal.clear_output()
                self.zone_solution_dual.clear_output()
                self.zone_curs_cout.clear_output()
                display(erreur= print("Il y a un problème avec les données rentrées. \nUn des lots n'est pas valide."))
        except ValueError:
            with self.zone_probleme:
                self.zone_probleme.clear_output()
                self.zone_solution_primal.clear_output()
                self.zone_solution_dual.clear_output()
                self.zone_curs_cout.clear_output()
                display(erreur= print("Il y a un problème avec les données rentrées. \nAssurez vous d'avoir correctement saisi les données."))

                
    def _sur_clique2(self, b):
        
        self.zone_probleme.clear_output()
        self.zone_solution_primal.clear_output()
        self.zone_solution_dual.clear_output()

        with self.zone_probleme:
            display(self.probleme.genere_table())
        with self.zone_solution_primal:
            display(resolution.tables_solutions(self.probleme, primal = True, frac = False))
        with self.zone_solution_dual:
            display(resolution.tables_solutions(self.probleme, primal = False, frac = False))
