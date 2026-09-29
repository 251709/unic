import tkinter as tk

from src.grid import Grid
from src.astar import AStar

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

        self.start_button = tk.Button(
            root,
            text="Запустить A*",
            command=self.start_astar,
        )
        self.start_button.pack(pady=(0, 10))

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

    def start_astar(self):
        """Запускает алгоритм A*."""
        self.start_button.config(state="disabled")

        astar = AStar(self.grid)
        self.path, self.visited_order = astar.find_path()

        self.current_step = 0

        self.animate_search()

    def animate_search(self):
        """Показывает процесс поиска по шагам."""
        if self.current_step >= len(self.visited_order):
            self.show_path()
            return

        row, col = self.visited_order[self.current_step]

        if (row, col) != self.grid.start and (row, col) != self.grid.end:
            self.draw_cell(row, col, "yellow")

        self.current_step += 1

        self.root.after(100, self.animate_search)

    def show_path(self):
        """Показывает найденный путь."""
        for row, col in self.path:
            if (row, col) != self.grid.start and (row, col) != self.grid.end:
                self.draw_cell(row, col, "green")

        self.start_button.config(state="normal")

    def draw_cell(self, row, col, color):
        """Перерисовывает одну клетку."""
        x1 = col * CELL_SIZE
        y1 = row * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE

        self.canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill=color,
            outline="gray",
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()