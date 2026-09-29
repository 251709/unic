class Grid:
    """Представляет сетку лабиринта."""

    def __init__(self, filename):
        """Загружает лабиринт из указанного файла."""
        self.cells = self._load(filename)
        self.start = self._find("S")
        self.end = self._find("E")

        self.rows = len(self.cells)
        self.cols = len(self.cells[0])

    def _load(self, filename):
        """Загружает строки лабиринта из текстового файла."""
        with open(filename, "r", encoding="utf-8") as file:
            return [line.rstrip("\n") for line in file]

    def _find(self, symbol):
        """Находит координаты клетки с указанным символом."""
        for row in range(len(self.cells)):
            for col in range(len(self.cells[row])):
                if self.cells[row][col] == symbol:
                    return row, col

        raise ValueError(f"Символ {symbol} не найден")

    def is_free(self, row, col):
        """Проверяет, является ли клетка проходимой."""
        return self.cells[row][col] != "#"

    def get_neighbors(self, row, col):
        """Возвращает соседние проходимые клетки."""
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]

        neighbors = []

        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc

            if (
                0 <= new_row < self.rows
                and 0 <= new_col < self.cols
                and self.is_free(new_row, new_col)
            ):
                neighbors.append((new_row, new_col))

        return neighbors