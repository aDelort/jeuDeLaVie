# Jeu de la Vie

Runs with Python3 only

Le Jeu de la Vie a été immaginé par Conway en 1970 (Conway's Game of Life). Il est régi par des règles très simples pour déterminer, à partir d'une génération n, la composition de la génération n+1. En théorie le jeu doit se dérouler sur une grille infinie, mais ces conditions sont évidemment impossibles sur un ordinateur.

Les règles sont les suivantes :
- Une cellule vivante entourée par exactement 2 ou 3 cellules vivantes reste vivante à la génération suivante, sinon elle meurt ;
- Une cellule morte entourée par exactement 3 cellules vivantes naît à la génération suivante, sinon elle reste morte.

Dans la grille, les cellules vivantes sont les cellules noires, tandis que les cellules mortes sont les cellules grises. Le clic gauche permet de faire naître une cellule, et le clic droit de tuer.
