'''
You are given a set of rectangles represented by (width, height), and a grid of size NxM.

Return a random possible configuration of the rectangles in the grid.
If no such configuration exists, return None.
'''
import random


class Cell:
    def __init__(self, top_left:tuple, width: int, height: int, parent = None):
        '''
        A cell is represented by its top left corner and its dimensions.
        A cell can contain child cells
        '''
        self.top_left: tuple = top_left # Top left corner
        self.dimensions: tuple = (width, height)
        self.parent: Cell = parent
        self.children: list[Cell] = []
        
    def area(self):
        '''
        Returns the area of the cell
        '''
        return self.dimensions[0] * self.dimensions[1]
    
    def corners(self):
        '''
        Returns a list of coordinates that represent the 4 corners of the cell
        '''
        x1 = self.top_left[0]
        x2 = self.top_left[0] + self.dimensions[0]
        y1 = self.top_left[1]
        y2 = self.top_left[1] + self.dimensions[1]
        
        return [(x1, y1), (x1, y2), (x2, y1), (x2, y2)]
    
    def contains_coord(self, coord: tuple):
        '''
        Return True if the cell contains this coord. False otherwise.
        '''
        x = coord[0]
        x_check = self.top_left[0] <= x <= (self.top_left[0] + self.dimensions[0])
        y = coord[1]
        y_check = self.top_left[1] <= y <= (self.top_left[1] + self.dimensions[1])
        
        return x_check and y_check
    
    def get_cell_by_coord(self, coord: tuple):
        '''
        Given a coord, Iterates over the cell and its children cells and returns the most bottom cell that contains it.
        Returns None if the coord is not in the cell or its children.
        '''
        if self.contains_coord(coord):
            # If the cell doesnt have child cells, the coord belongs to this cell
            if not self.children:
                return self
            
            # If the cell has child cells, iterate over them and find the cell that contains the coord
            for c in self.children:
                res = c.get_cell_by_coord(coord)
                if res:
                    return res
                
        return None
        
    def can_contain(self, c):
        '''
        Returns true if this cell is able to contain the entirety of the input cell.
        '''
        tl = self.corners()[0] # Top left
        br = c.corners()[3] # Bottom right
        return self.contains_coord(tl) and self.contains_coord(br) # If the top left and bottom right corners are contained in the cell, then the entire cell is also contained
        
    def insert(self, c):
        '''
        Inserts the input cell as a child of this cell and updates the parent of the child cell.
        '''
        self.children.append(c)
        c.parent = self
        # Add division into more child cells here
        
    def __str__(self):
        s = f'{self.__class__.__name__}: {self.top_left}\n'
        s += f'Size - {self.dimensions}\n'
        return s
        
    def __repr__(self):
        s = self.__str__()
        s += f'Children [ \n'
        for c in self.children:
            s += c.__repr__()
        s += ']'
        return s

class Rect(Cell):
    def __init__(self, top_left, width, height, parent=None):
        '''
        A Rect is a Cell that can't have child Cells.
        The Rect can be moved in its parent Cell.
        '''
        super().__init__(top_left, width, height, parent)
        
    def flip(self):
        '''
        Flips the dimensions of the rectangle
        '''
        self.dimensions = self.dimensions[::-1]
        
    def place(self, x, y):
        '''
        Places the Rect at the given coordinates
        '''
        self.top_left = (x, y)
        
    def __repr__(self):
        return super().__repr__()
    
class Grid:
    def __init__(self, n: int, m: int):
        self.root = Cell((0, 0), n, m)
        
    def place_rect(self, r: Rect, coord: tuple):
        c = self.root.get_cell_by_coord(coord) # Find the bottom most cell that contains the desired coord
        if not c.can_contain(r):
            r.flip()
            if not c.can_contain(r):
                return False
        
        r.top_left = coord
        c.insert(r)
        
    def __repr__(self):
        return self.root.__repr__()
        
            
    
def generate_rects(num, max_length = 5):
    '''
    Generates and returns num amount of rectangles with random dimensions.
    '''
    rects = []
    for _ in range(num):
        x = random.randrange(1, max_length)
        y = random.randrange(1, max_length)
        rects.append(Rect((-1, -1), x, y))
        
    return rects

# r = generate_rects(5)
# print(r)
# r[0].flip()
# r[0].place(5, 5)
# print(r)

# g = Grid(10, 10)
# r = Rect((0,0), 10, 5)
# g.place_rect(r, (0, 0))
# print(g)


