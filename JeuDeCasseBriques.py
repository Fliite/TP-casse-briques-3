import tkinter as tk
from jeu import JeuCasseBrique

if __name__ == "__main__":
    root = tk.Tk()
    game = JeuCasseBrique(root)
    root.mainloop()