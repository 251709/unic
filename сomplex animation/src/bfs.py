from collections import deque


class BFS:
    """Реализует поиск в ширину."""

    def __init__(self, grid):
        """Создаёт алгоритм для указанной сетки."""
        self.grid = grid

    def find_path(self):
        """Находит кратчайший путь от начала до конца."""
        start = self.grid.start
        end = self.grid.end

        queue = deque([start])
        came_from = {start: None}
        visited_order = []

        while queue:
            current = queue.popleft()

            if current in visited_order:
                continue

            visited_order.append(current)

            if current == end:
                path = self._build_path(came_from, end)
                return path, visited_order

            for neighbor in self.grid.get_neighbors(*current):
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    queue.append(neighbor)

        return [], visited_order

    def _build_path(self, came_from, current):
        """Восстанавливает найденный путь."""
        path = []

        while current is not None:
            path.append(current)
            current = came_from[current]

        path.reverse()

        return path