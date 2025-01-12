'''
You are given a set of rectangles represented by (width, height), and a grid of size NxM.

Return a random possible configuration of the rectangles in the grid.
If no such configuration exists, return None.
'''
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class Cell:
    def __init__(self, top_left:tuple, width: int, height: int, parent = None):
        '''
        A cell is represented by its top left corner, width and height.
        
        Cells with width or height == 0 will return None
        '''
        if width <= 0 or height <= 0:
            return None
        
        self.top_left: tuple = top_left # Top left corner
        self.width = width
        self.height = height
        self.min_x = top_left[0]
        self.min_y = top_left[1]
        self.max_x = top_left[0] + self.width
        self.max_y = top_left[1] + self.height
        
    def area(self):
        '''
        Returns the area of the cell
        '''
        return self.width * self.height
    
    def contains_coord(self, coord: tuple):
        '''
        Return True if the cell contains this coord. False otherwise.
        '''
        x = coord[0]
        x_check = self.top_left[0] <= x <= (self.top_left[0] + self.width)
        y = coord[1]
        y_check = self.top_left[1] <= y <= (self.top_left[1] + self.height)
        
        return x_check and y_check
    
    def can_contain(self, c):
        '''
        Returns true if this cell is able to contain the entirety of the input cell.
        '''
        tl = self.corners()[0] # Top left
        br = c.corners()[3] # Bottom right
        return self.contains_coord(tl) and self.contains_coord(br) # If the top left and bottom right corners are contained in the cell, then the entire cell is also contained
        
    def __str__(self):
        s = f'{self.__class__.__name__}: {self.top_left}\n'
        s += f'Size - {self.width}, {self.height}\n'
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
        self.width, self.height = self.height, self.width
        
    def place(self, x, y):
        '''
        Places the Rect at the given coordinates
        '''
        self.top_left = (x, y)
        
    def __repr__(self):
        return super().__repr__()
    
class Grid:
    def __init__(self, n: int, m: int):
        self.cells: list[Cell] = [Cell((0, 0), n, m)] # Create the main cell
       
    def subdivide(self, c: Cell, r: Rect):
        # Subdivides a cell based on the corners of a rectangle
        top = Cell(c.top_left, c.width, r.min_y - c.min_y)
        left = Cell((c.min_x, r.min_y), r.min_x - c.min_x, r.height)
        right = Cell((r.max_x, r.min_x), c.max_x - r.max_x, r.height)
        bottom = Cell((c.min_x, r.max_y), c.width, c.max_y - r.max_y)
        
        # Remove the partitioned cell from the list
        self.cells.remove(c)
        
        # Add the new cells if they are valid
        for new_cell in [top, left, right, bottom]:
            if new_cell:
                self.cells.append(new_cell)
    
    def place_rect(self, r: Rect, coord: tuple):
        
        for c in self.cells:
            # Iterate over all cells in the grid
            
            if c.can_contain(r):
                # If the rectangle fits in the cell, partition the cell into 4 cells that don't include the rectangle.
                
                r.place(c.top_left) # Place the rectangle at the corner of cell
                self.subdivide(c, r) # Subdivide the cell
                
                return True
            
        # Return False since the rect couldn't be placed
        return False
        
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

#define Matplotlib figure and axis
fig, ax = plt.subplots()
ax.plot(20, 20)

#add rectangle to plot
ax.add_patch(Rectangle((1, 1), 8, 8,))

# Enable grid lines
ax.grid()

#display plot
plt.show()
