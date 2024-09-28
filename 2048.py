import tkinter as tk
import random

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game")
        self.grid_size = 4
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.add_new_tile()
        self.add_new_tile()

        self.canvas = tk.Canvas(master, width=400, height=400, bg="lightgrey")
        self.canvas.pack()
        self.draw_grid()

        master.bind("<Key>", self.key_handler)

    def add_new_tile(self):
        empty_tiles = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size) if self.grid[r][c] == 0]
        if empty_tiles:
            row, col = random.choice(empty_tiles)
            self.grid[row][col] = random.choice([2, 4])

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                value = self.grid[r][c]
                x1, y1 = c * 100 + 5, r * 100 + 5
                x2, y2 = x1 + 90, y1 + 90
                color = self.get_tile_color(value)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(value) if value != 0 else "", font=("Helvetica", 24))

    def get_tile_color(self, value):
        colors = {
            0: "lightgrey",
            2: "#EEE4DA",
            4: "#EDE0C8",
            8: "#F2B179",
            16: "#F59563",
            32: "#F67C5F",
            64: "#F67C5F",
            128: "#EDCF72",
            256: "#EDCC61",
            512: "#EDC850",
            1024: "#EDC53F",
            2048: "#EDC22E"
        }
        return colors.get(value, "black")

    def key_handler(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            self.move(event.keysym)
            self.add_new_tile()
            self.draw_grid()

    def move(self, direction):
        if direction == "Right":
            for r in range(self.grid_size):
                self.grid[r] = self.merge(self.grid[r][::-1])[::-1]
        elif direction == "Left":
            for r in range(self.grid_size):
                self.grid[r] = self.merge(self.grid[r])
        elif direction == "Down":
            for c in range(self.grid_size):
                column = [self.grid[r][c] for r in range(self.grid_size)]
                column = self.merge(column[::-1])[::-1]
                for r in range(self.grid_size):
                    self.grid[r][c] = column[r]
        elif direction == "Up":
            for c in range(self.grid_size):
                column = [self.grid[r][c] for r in range(self.grid_size)]
                column = self.merge(column)
                for r in range(self.grid_size):
                    self.grid[r][c] = column[r]

    def merge(self, tiles):
        new_tiles = [x for x in tiles if x != 0]
        merged = []
        skip = False

        for i in range(len(new_tiles)):
            if skip:
                skip = False
                continue
            if i + 1 < len(new_tiles) and new_tiles[i] == new_tiles[i + 1]:
                merged.append(new_tiles[i] * 2)
                skip = True
            else:
                merged.append(new_tiles[i])

        while len(merged) < len(tiles):
            merged.append(0)

        return merged

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()