class Brique:
    def __init__(self, canvas, x1, y1, x2, y2, color="orange", hits=1):
        self.canvas = canvas
        self.hits = hits
        self.id = canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def destroy(self):
        try:
            self.canvas.delete(self.id)
        except Exception:
            pass