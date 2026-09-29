import tkinter as tk

from src.grid import Grid

CELL_SIZE = 30

class Application:
    """Главное окно приложения."""

    def __init__(self, root):
        """Создаёт интерфейс приложения."""
        self.root = root
        self.root.title("Поиск кратчайшего пути")
        self.root.resizable(False, False)

        self.grid = Grid("maze.txt")

        self.canvas = tk.Canvas(
            root,
            width=self.grid.cols * CELL_SIZE,
            height=self.grid.rows * CELL_SIZE,
            bg="white",
        )
        self.canvas.pack(padx=10, pady=10)

        self.draw_grid()

    def draw_grid(self):
        """Отрисовывает лабиринт."""
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                cell = self.grid.cells[row][col]

                if cell == "#":
                    fill = "black"
                elif cell == "S":
                    fill = "blue"
                elif cell == "E":
                    fill = "red"
                else:
                    fill = "white"

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=fill,
                    outline="gray",
                )


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()