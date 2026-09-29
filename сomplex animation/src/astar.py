class AStar:
    """Реализует алгоритм поиска A*."""

    def __init__(self, grid):
        """Создаёт алгоритм для указанной сетки."""
        self.grid = grid

    def heuristic(self, current, target):
        """Вычисляет манхэттенское расстояние между клетками."""
        row1, col1 = current
        row2, col2 = target

        return abs(row1 - row2) + abs(col1 - col2)

    def find_path(self):
        """Находит кратчайший путь от начала до конца."""
        start = self.grid.start
        end = self.grid.end

        queue = [start]

        came_from = {start: None}
        cost = {start: 0}

        while queue:
            # Ищем клетку с минимальным приоритетом
            current = min(
                queue,
                key=lambda cell: (
                    cost[cell] + self.heuristic(cell, end)
                )
            )

            queue.remove(current)

            if current == end:
                return self._build_path(came_from, end)

            for neighbor in self.grid.get_neighbors(*current):
                new_cost = cost[current] + 1

                if (
                    neighbor not in cost
                    or new_cost < cost[neighbor]
                ):
                    cost[neighbor] = new_cost
                    queue.append(neighbor)
                    came_from[neighbor] = current

        return []

    def _build_path(self, came_from, current):
        """Восстанавливает найденный путь."""
        path = []

        while current is not None:
            path.append(current)
            current = came_from[current]

        path.reverse()

        return path