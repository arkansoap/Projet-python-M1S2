#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Application permettant la résolution de programme dual.
"""
import typer
from sys import stdin
from pathlib import Path
from rich.console import Console
from prog_dual import probleme, resolution

app = typer.Typer(help="Application résolvant des programmes duals liés à la vente d'armes.")


@app.command("std")
def par_entree_standard(mode):
    """Résout le problème dual à partir de l'entrée standard.
    Choix de l'option de résolution : lp ou pulp
    """
    cs = Console()
    entree = "".join([ligne for ligne in stdin])
    prob = probleme.Probleme.par_str(entree)
    cs.print(prob.genere_table())
    cs.print(resolution.affichage_solutions(prob, frac))


@app.command("fch")
def par_fichier(
    frac : bool,
    fichier: str = typer.Argument(..., help="nom du fichier décrivant le problème")):
    """Résout le problème dual à patir d'un fichier.
    Choix de l'option de résolution : lp ou pulp
    """
    cs = Console()
    entree = Path(fichier).read_text()
    prob = probleme.Probleme.par_str(entree)
    cs.print(prob.genere_table())
    cs.print(resolution.affichage_solutions(prob, frac))


if __name__ == "__main__":
    app()