import random


class Minesweeper:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.mineholder = []
        self.generate_mines()
        self.completed = False
        self.count_opened_cell = 0
        self.game_id = None

    def generate_mines(self):
        placed_mines = 0
        while placed_mines < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if f"{row}{col}" not in self.mineholder:
                self.mineholder.append(f"{row}{col}")
                placed_mines += 1

    def count_adjacent_mines(self, row, col):
        count = 0
        directions = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if (i != 0 or j != 0)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols and f"{r}{c}" in self.mineholder:
                count += 1
        return count

    def open_cell(self, row, col):
        self.count_opened_cell += 1
        if f"{row}{col}" in self.mineholder:
            self.game_over()
            return False
        else:
            mines_nearby = self.count_adjacent_mines(row, col)
            self.board[row][col] = str(mines_nearby)
            if mines_nearby == 0:
                self.reveal_empty_cells(row, col)
        if self.count_opened_cell >= self.cols * self.rows - self.mines:
            self.win()

    def reveal_empty_cells(self, row, col):
        directions = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if (i != 0 or j != 0)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == ' ':
                self.open_cell(r, c)

    def game_over(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if f"{r}{c}" in self.mineholder:
                    self.board[r][c] = 'X'
                else:
                    mines_nearby = self.count_adjacent_mines(r, c)
                    self.board[r][c] = str(mines_nearby)
                    if mines_nearby == 0:
                        self.reveal_empty_cells(r, c)
        self.completed = True

    def win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if f"{r}{c}" in self.mineholder:
                    self.board[r][c] = 'M'
        self.completed = True

