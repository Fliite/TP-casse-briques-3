class Brique:
    '''Dans cette classe, on gère les briques du jeu.
    On initialise une brique avec ses coordonnées, sa couleur et le nombre de coups nécessaires pour la détruire.
    On pourra eventuellement modifier cette classe pour ajouter des fonctionnalités comme des briques spéciales (indestructibles, qui donnent des bonus, etc.).
    '''
    def __init__(self, canvas, x1, y1, x2, y2, color="orange", hits=1):
        self.canvas = canvas
        self.hits = hits
        self.id = canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def destroy(self):
        try:
            self.canvas.delete(self.id)
        except Exception:
            pass