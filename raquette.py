class Raquette:
    def __init__(self, canvas, x, y, width=100, height=12, color="lightblue", speed=9):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.id = canvas.create_rectangle(x - width/2, y - height/2, x + width/2, y + height/2, fill=color, outline=color)
        self.vitesse = speed
        self.vx = 0

    def move(self):
        self.canvas.move(self.id, self.vx, 0)
        # clamp to canvas
        x1, y1, x2, y2 = self.coords()
        W = int(self.canvas['width'])
        if x1 < 0:
            self.canvas.move(self.id, -x1, 0)
        elif x2 > W:
            self.canvas.move(self.id, W - x2, 0)

    def coords(self):
        return self.canvas.coords(self.id)

    def center(self):
        x1, y1, x2, y2 = self.coords()
        return ((x1 + x2) / 2, (y1 + y2) / 2)

    def set_position_center(self, x):
        x1, y1, x2, y2 = self.coords()
        cx = (x1 + x2) / 2
        dx = x - cx
        self.canvas.move(self.id, dx, 0)

    def GoRaquette(self, vx):
        self.vx = vx