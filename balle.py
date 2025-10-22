import math

class Balle:
    def __init__(self, canvas, x, y, r=7, color="white", vitesseBalle=6):
        self.canvas = canvas
        self.r = r
        self.id = canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=color)
        self.vitesseBalle = vitesseBalle
        self.vx = vitesseBalle * 0.7
        self.vy = -abs(vitesseBalle * 0.7)
        self._prev_bbox = self.canvas.coords(self.id)

    def coords(self):
        ''' Renvoie les coordonnées actuelles de la balle sous la forme (x1, y1, x2, y2) '''
        return self.canvas.coords(self.id)

    def move(self):
        ''' Déplace la balle selon sa vitesse '''
        self._prev_bbox = self.coords()
        self.canvas.move(self.id, self.vx, self.vy)

    def Position(self, x, y):
        ''' Permet de positionner la balle aux coordonnées (x, y) 
         en déplaçant la balle de sa position actuelle à la nouvelle position
        '''
        x1, y1, x2, y2 = self.coords()
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        dx = x - cx
        dy = y - cy
        self.canvas.move(self.id, dx, dy)
        self._prev_bbox = self.coords()

    def VerifierVitesse(self, vx=None, vy=None):
        ''' Permet de modifier la vitesse de la balle 
        elle prend en argument la nouvelle vitesse en x et/ou y
        '''
        if vx is not None: self.vx = vx
        if vy is not None: self.vy = vy

    def RebondX(self):
        ''' Inverse la vitesse en x de la balle '''
        self.vx = -self.vx

    def RebondY(self):
        ''' Inverse la vitesse en y de la balle '''
        self.vy = -self.vy

    def vitesseBalle_set(self, vitesseBalle):
        ''' Modifie la vitesse de la balle en conservant son angle de déplacement '''
        signx = 1 if self.vx >= 0 else -1
        signy = 1 if self.vy >= 0 else -1
        ang = math.atan2(abs(self.vy), abs(self.vx))
        self.vx = signx * vitesseBalle * math.cos(ang)
        self.vy = signy * vitesseBalle * math.sin(ang)
        self.vitesseBalle = vitesseBalle

    def RebondRaquette(self, paddle_bbox, max_angle_deg=75):
        '''Permet de gérer le rebond de la balle sur la raquette en fonction de la position d'impact'''
        bx1, by1, bx2, by2 = self.coords()
        RaquetteX1, paddle_y1, RaquetteX2, paddle_y2 = paddle_bbox
        CentreBalle = (bx1 + bx2) / 2 # C'est le centre de la balle
        CentreR = (RaquetteX1 + RaquetteX2) / 2 # C'est le centre de la raquette
        CentreRaquette = (RaquetteX2 - RaquetteX1) / 2
        if CentreRaquette == 0: 
            PosRelative = 0 
        else:
            PosRelative = max(-1.0, min(1.0, (CentreBalle - CentreR) / CentreRaquette))
        angle = math.radians(PosRelative * max_angle_deg)
        vitesseBalle = math.hypot(self.vx, self.vy)
        self.vx = vitesseBalle * math.sin(angle)
        self.vy = -abs(vitesseBalle * math.cos(angle))

    def prev_bbox(self):
        ''' Renvoie les coordonnées précédentes de la balle sous la forme (x1, y1, x2, y2) '''
        return self._prev_bbox