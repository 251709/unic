import tkinter as tk
from tkinter import filedialog, messagebox

from src.grid import Grid
from src.astar import AStar
from src.bfs import BFS
from src.dfs import DFS

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

        self.create_controls()
        self.draw_grid()

    def create_controls(self):
        """Создаёт элементы управления."""
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=(0, 10))

        self.algorithm_label = tk.Label(
            self.control_frame,
            text="Алгоритм:",
        )
        self.algorithm_label.pack(side="left", padx=5)

        self.algorithm = tk.StringVar(value="A*")

        self.algorithm_menu = tk.OptionMenu(
            self.control_frame,
            self.algorithm,
            "A*",
            "BFS",
            "DFS",
        )
        self.algorithm_menu.pack(side="left", padx=5)

        self.start_button = tk.Button(
            self.control_frame,
            text="Запустить",
            command=self.start_algorithm,
        )
        self.start_button.pack(side="left", padx=5)

        self.load_button = tk.Button(
            self.control_frame,
            text="Загрузить лабиринт",
            command=self.load_maze,
        )
        self.load_button.pack(side="left", padx=5)

    def load_maze(self):
        """Загружает лабиринт из текстового файла."""
        filename = filedialog.askopenfilename(
            title="Выберите файл лабиринта",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Все файлы", "*.*"),
            ],
        )

        if not filename:
            return

        try:
            self.grid = Grid(filename)

            self.canvas.config(
                width=self.grid.cols * CELL_SIZE,
                height=self.grid.rows * CELL_SIZE,
            )

            self.canvas.delete("all")
            self.draw_grid()

        except (ValueError, IndexError) as error:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось загрузить лабиринт:\n{error}",
            )

    def reset_grid(self):
        """Очищает результаты предыдущего поиска."""
        self.canvas.delete("all")
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

    def start_algorithm(self):
        """Запускает выбранный алгоритм."""
        self.reset_grid()

        self.start_button.config(state="disabled")
        self.load_button.config(state="disabled")

        algorithm_name = self.algorithm.get()

        if algorithm_name == "A*":
            algorithm = AStar(self.grid)
        elif algorithm_name == "BFS":
            algorithm = BFS(self.grid)
        else:
            algorithm = DFS(self.grid)

        self.path, self.visited_order = algorithm.find_path()

        self.current_step = 0

        self.animate_search()

    def animate_search(self):
        """Показывает процесс поиска по шагам."""
        if self.current_step >= len(self.visited_order):
            self.show_path()
            return

        if self.current_step > 0:
            prev_row, prev_col = self.visited_order[
                self.current_step - 1
            ]

            if (
                (prev_row, prev_col) != self.grid.start
                and (prev_row, prev_col) != self.grid.end
            ):
                self.draw_cell(
                    prev_row,
                    prev_col,
                    "lightblue",
                )

        row, col = self.visited_order[self.current_step]

        if (
            (row, col) != self.grid.start
            and (row, col) != self.grid.end
        ):
            self.draw_cell(
                row,
                col,
                "yellow",
            )

        self.current_step += 1

        self.root.after(100, self.animate_search)

    def show_path(self):
        """Показывает найденный путь."""
        if not self.path:
            messagebox.showinfo(
                "Результат",
                "Путь от начала до конца не найден.",
            )

            self.start_button.config(state="normal")
            self.load_button.config(state="normal")
            return

        for row, col in self.path:
            if (
                (row, col) != self.grid.start
                and (row, col) != self.grid.end
            ):
                self.draw_cell(
                    row,
                    col,
                    "green",
                )

        self.start_button.config(state="normal")
        self.load_button.config(state="normal")

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