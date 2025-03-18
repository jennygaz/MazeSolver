class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y 
    

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.start.x, self.start.y,
            self.end.x, self.end.y,
            fill=fill_color,
            width=2
        )

class Cell:
    TOP_WALL      = 0b1000
    BOTTOM_WALL   = 0b0010
    LEADING_WALL  = 0b0001
    TRAILING_WALL = 0b0100
    # Walls is a bitmask with 4 bits representing the 4 walls of the cell
    # from left to right: top, right, bottom, left
    def __init__(self, window=None, walls=0b1111):
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._window = window
        self.visited = False
        self.walls = walls

    def has_leading_wall(self):
        return self.walls & Cell.LEADING_WALL

    def has_trailing_wall(self):
        return self.walls & Cell.TRAILING_WALL
    
    def has_top_wall(self):
        return self.walls & Cell.TOP_WALL
    
    def has_bottom_wall(self):
        return self.walls & Cell.BOTTOM
    
    def add_leading_wall(self):
        self.walls |= Cell.LEADING_WALL
    
    def add_trailing_wall(self):
        self.walls |= Cell.TRAILING_WALL

    def add_top_wall(self):
        self.walls |= Cell.TOP_WALL

    def add_bottom_wall(self):
        self.walls |= Cell.BOTTOM_WALL
    
    def remove_leading_wall(self):
        self.walls &= ~Cell.LEADING_WALL
    
    def remove_trailing_wall(self):
        self.walls &= ~Cell.TRAILING_WALL
    
    def remove_top_wall(self):
        self.walls &= ~Cell.TOP_WALL

    def remove_bottom_wall(self):
        self.walls &= ~Cell.BOTTOM_WALL
    
    def draw(self, x1, y1, x2, y2):
        if self._window is None: return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.walls & Cell.TOP_WALL:
            self._window.draw_line(
                Line(Point(x1, y1), Point(x2, y1)),
                "black"
            )
        if self.walls & Cell.BOTTOM_WALL:
            self._window.draw_line(
                Line(Point(x1, y2), Point(x2, y2)),
                "black"
            )
        if self.walls & Cell.LEADING_WALL:
            self._window.draw_line(
                Line(Point(x1, y1), Point(x1, y2)),
                "black"
            )
        if self.walls & Cell.TRAILING_WALL:
            self._window.draw_line(
                Line(Point(x2, y1), Point(x2, y2)),
                "black"
            )
    
    def draw_move(self, to_cell, undo=False):
        lhs_center = Point((self._x1 + self._x2) // 2, (self._y1 + self._y2) // 2)
        rhs_center = Point((to_cell._x1 + to_cell._x2) // 2, (to_cell._y1 + to_cell._y2) // 2)
        line = Line(lhs_center, rhs_center)
        fill_color = 'gray' if undo else 'red'
        self._window.draw_line(line, fill_color)