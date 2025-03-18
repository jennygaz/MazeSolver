from geometry import Cell
import random, time

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        if seed: random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
    
    def _draw_cell(self, i, j):
        if self._win is None: return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None: return
        self._win.redraw()
        time.sleep(0.1)

    def _break_entrance_and_exit(self):
        self._cells[0][0].walls &= ~Cell.TOP_WALL
        self._cells[self._num_cols - 1][self._num_rows - 1].walls &= ~Cell.BOTTOM_WALL
        self._cells[0][0]

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []
            if i > 0 and not self.cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))
            
            if len(next_index_list) == 0:
                self._draw_cell(i, j)
                return

            direction = random.randrange(len(next_index_list))
            next = next_index_list[direction]

            if next[0] == i + 1:
                self._cells[i][j].remove_trailling_wall()
                self._cells[i + 1][j].remove_leading_wall()
            if next[0] == i - 1:
                self._cells[i][j].remove_leading_wall()
                self._cells[i - 1][j].remove_trailling_wall()
            if next[1] == j + 1:
                self._cells[i][j].remove_bottom_wall()
                self._cells[i][j + 1].remove_top_wall()
            if next[1] == j - 1:
                self._cells[i][j].remove_top_wall()
                self._cells[i][j - 1].remove_bottom_wall()
            
            self._break_walls_r(next[0], next[1])
    
    def _reset_cells_visited(self):
        for column in self._cells:
            for cell in column:
                cell.visited = False

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True

        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        if i > 0 and not self._cells[i][j].has_leading_wall() and not self._cells[i - 1][j].visited:
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j): return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)
        
        if i < self._num_cols - 1 and not self._cells[i][j].has_trailling_wall() and not self._cells[i + 1][j].visited:
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j): return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        if j > 0 and not self._cells[i][j].has_top_wall() and not self._cells[i][j - 1].visited:
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1): return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)

        if j < self._num_rows - 1 and not self._cells[i][j].has_bottom_wall() and not self._cells[i][j + 1].visited:
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1): return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        return False
    
    def solve(self):
        self._solve_r(0, 0)