import tkinter as tk
from tkinter import messagebox
from balle import Balle
from raquette import Raquette
from brique import Brique

class JeuCasseBrique:
    def __init__(self, racine):
        '''Initialise le jeu : fenêtre, canevas, contrôles et objets du jeu.'''
        # référence à la fenêtre principale
        self.Racine = racine
        # titre de la fenêtre
        self.Racine.title("Jeu de casse-briques")
        # On peut changer les dimensions du canevas à sa guise
        self.Largeur, self.Hauteur = 900, 600
        # création du canevas où tout est dessiné
        self.Canevas = tk.Canvas(self.Racine, width=self.Largeur, height=self.Hauteur, bg="black")
        self.Canevas.pack()

        # barre d'outils en haut pour boutons et affichage
        self.HautFrame = tk.Frame(self.Racine)
        self.HautFrame.pack(fill="x")
        # bouton démarrer
        self.DemarerBtn = tk.Button(self.HautFrame, text="Démarrer", command=self.Demarer)
        self.DemarerBtn.pack(side="left", padx=5, pady=3)
        # bouton quitter
        self.QuitterBtn = tk.Button(self.HautFrame, text="Quitter", command=self.Racine.quit)
        self.QuitterBtn.pack(side="left", padx=5, pady=3)
        # variables Tk pour score et vies
        self.ScoreVar = tk.IntVar(value=0)
        self.ViesVar = tk.IntVar(value=3)
        tk.Label(self.HautFrame, text="Score:").pack(side="left", padx=(20,0))
        tk.Label(self.HautFrame, textvariable=self.ScoreVar).pack(side="left")
        tk.Label(self.HautFrame, text="  Vies:").pack(side="left", padx=(20,0))
        tk.Label(self.HautFrame, textvariable=self.ViesVar).pack(side="left")

        # initialisation des objets du jeu (raquette, balle, briques)
        self.InitObjets()
        # indicateur si la boucle de jeu tourne
        self.Running = False
        # liaisons des touches clavier
        self.LierTouches()
        # délai entre ticks en ms (~60 FPS)
        self._TauxTick = 16
        # démarre la boucle périodique
        self.Boucle()

    def InitObjets(self):
        '''Crée la raquette, la balle, réinitialise le score/vies et crée les briques.'''
        # raquette positionnée au centre bas
        self.Raquette = Raquette(self.Canevas, self.Largeur/2, self.Hauteur - 40)
        # balle positionnée juste au-dessus de la raquette
        self.Balle = Balle(self.Canevas, self.Largeur/2, self.Hauteur - 60)
        # dictionnaire id_canvas -> brique
        self.Briques = {}
        # réinitialisation des compteurs
        self.ScoreVar.set(0)
        self.ViesVar.set(3)
        # création des briques
        self.CreerBriques()

    def CreerBriques(self, lignes=1, colonnes=10, espace=2, EspaceSuperieur=50):
        '''Crée une grille de briques en haut du canevas.'''
        # calcul en tenant compte de la taille de la fenetre
        LBrique = (self.Largeur - espace * (colonnes + 1)) / colonnes
        # hauteur fixe des briques
        HBrique = 22
        # palette de couleurs par ligne
        couleurs = ["red","orange","yellow","green","cyan","lightgreen"]
        for r in range(lignes):
            for c in range(colonnes):
                # coordonnées de la brique
                x1 = espace + c * (LBrique + espace)
                y1 = EspaceSuperieur + r * (HBrique + espace)
                x2 = x1 + LBrique
                y2 = y1 + HBrique
                # création de l'objet Brique et stockage par id canvas
                brique = Brique(self.Canevas, x1, y1, x2, y2, color=couleurs[r % len(couleurs)])
                self.Briques[brique.id] = brique

    def LierTouches(self):
        '''Lie les touches clavier aux actions de la raquette et du jeu.'''
        # flèche gauche -> mouvement gauche
        self.Racine.bind("<KeyPress-Left>", lambda e: self.Raquette.GoRaquette(-self.Raquette.vitesse))
        # flèche droite -> mouvement droite
        self.Racine.bind("<KeyPress-Right>", lambda e: self.Raquette.GoRaquette(self.Raquette.vitesse))
        # relâchement de la touche gauche
        self.Racine.bind("<KeyRelease-Left>", lambda e: self.StopRaquette(-self.Raquette.vitesse))
        # relâchement de la touche droite
        self.Racine.bind("<KeyRelease-Right>", lambda e: self.StopRaquette(self.Raquette.vitesse))
        # espace -> démarrer/relancer la partie
        self.Racine.bind("<space>", lambda e: self.Demarer())

    def StopRaquette(self, expect):
        '''Arrête la raquette uniquement si sa vitesse correspond à la direction attendue.'''
        # évite d'arrêter la raquette si l'autre touche est encore maintenue
        if self.Raquette.vx == expect:
            self.Raquette.GoRaquette(0)

    def Demarer(self):
        '''Démarre la boucle du jeu. Si pas de briques, réinitialise le plateau.'''
        # si la boucle n'était pas en cours, on la lance
        if not self.Running:
            self.Running = True
            # si toutes les briques ont été détruites, on réinitialise l'écran
            if not self.Briques:
                self.Canevas.delete("all")
                self.InitObjets()
            # positionne la balle au-dessus de la raquette
            px, py = self.Raquette.center()
            self.Balle.set_position(px, py - 30)
            # petite vitesse initiale
            self.Balle.reset_velocity(vx=self.Balle.vitesseBalle * 0.6, vy=-abs(self.Balle.vitesseBalle * 0.6))

    def Boucle(self):
        '''Boucle périodique qui met à jour l'état du jeu quand il tourne.'''
        # si le jeu est en cours, on met à jour une frame
        if self.Running:
            self.Update()
        # réenclenche la boucle après _TauxTick ms
        self.Racine.after(self._TauxTick, self.Boucle)

    def Update(self):
        '''Met à jour la position des objets et gère les collisions et la sortie.'''
        # déplacement de la raquette selon sa vitesse
        self.Raquette.move()
        # déplacement de la balle
        self.Balle.move()
        # collisions avec les murs
        self.CollisionsMur()
        # collisions avec la raquette
        self.CollisionsPaddle()
        # collisions avec les briques
        self.CollisionsBriques()
        # vérifie si la balle est sortie par le bas
        self.VerifierSortie()

    def CollisionsMur(self):
        '''Gère la réflexion de la balle sur les bords du canevas.'''
        # coordonnées actuelles de la balle
        x1, y1, x2, y2 = self.Balle.coords()
        # collision gauche
        if x1 <= 0 and self.Balle.vx < 0:
            self.Balle.RebondX()
        # collision droite
        if x2 >= self.Largeur and self.Balle.vx > 0:
            self.Balle.RebondX()
        # collision haut
        if y1 <= 0 and self.Balle.vy < 0:
            self.Balle.RebondY()

    def CollisionsPaddle(self):
        '''Gère les collisions entre la balle et la raquette.'''
        # trouve les objets qui chevauchent la balle
        items = self.Canevas.find_overlapping(*self.Balle.coords())
        paddle_id = self.Raquette.id
        # si on touche la raquette et que la balle descend
        if paddle_id in items and self.Balle.vy > 0:
            # réflexion selon la règle d'angle de la raquette
            self.Balle.RebondRaquette(self.Raquette.coords())

            # on repositionne la balle au-dessus de la raquette pour éviter qu'elle colle
            bx1, by1, bx2, by2 = self.Balle.coords()
            px1, py1, px2, py2 = self.Raquette.coords()
            overlap = by2 - py1
            if overlap > 0:
                self.Canevas.move(self.Balle.id, 0, -overlap - 1)

    def CollisionsBriques(self):
        '''Gère les collisions entre la balle et les briques et supprime les briques touchées.'''
        collided = []
        # récupère les items qui chevauchent la balle
        for item in self.Canevas.find_overlapping(*self.Balle.coords()):
            if item in self.Briques:
                collided.append(item)
        for bid in collided:
            brique = self.Briques.get(bid)
            if not brique:
                continue
            # calcul des recouvrements pour déterminer l'axe de réflexion
            bb = self.Balle.coords()
            brect = self.Canevas.coords(bid)
            ox = max(0, min(bb[2], brect[2]) - max(bb[0], brect[0]))
            oy = max(0, min(bb[3], brect[3]) - max(bb[1], brect[1]))
            if ox > oy:
                # plus de recouvrement horizontal -> inversion verticale
                self.Balle.RebondY()
            else:
                # sinon inversion horizontale
                self.Balle.RebondX()
            # destruction de la brique touchée
            brique.destroy()
            del self.Briques[bid]
            # augmentation du score
            self.ScoreVar.set(self.ScoreVar.get() + 10)
            # si plus de briques, victoire
            if not self.Briques:
                self.Victoire()
            # on gère au plus une brique par frame pour éviter des réflexions multiples
            break

    def VerifierSortie(self):
        '''Vérifie si la balle est sortie par le bas et gère la perte de vie / reset.'''
        x1, y1, x2, y2 = self.Balle.coords()
        # si la balle est sortie en bas
        if y1 > self.Hauteur:
            vies = self.ViesVar.get() - 1
            self.ViesVar.set(vies)
            # pause de la boucle jusqu'au redémarrage
            self.Running = False
            if vies <= 0:
                # si plus de vies -> défaite
                self.Defaite()
            else:
                # repositionne la balle et attend l'utilisateur pour redémarrer
                px, py = self.Raquette.center()
                self.Balle.set_position(px, py - 30)

    def Victoire(self):
        '''Affiche la boîte de dialogue de victoire et arrête le jeu.'''
        self.Running = False
        messagebox.showinfo("Victoire", f"Bravo ! Score: {self.ScoreVar.get()}")
        # on conserve le canevas pour permettre de relancer

    def Defaite(self):
        '''Affiche la boîte de dialogue de défaite et réinitialise le jeu.'''
        messagebox.showinfo("Défaite", f"Perdu ! Score: {self.ScoreVar.get()}")
        # réinitialisation du canevas et des objets
        self.Canevas.delete("all")
        self.InitObjets()