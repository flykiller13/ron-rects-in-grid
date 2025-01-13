'''
You are given a set of rectangles represented by (width, height), and a grid of size NxM.

Return a random possible configuration of the rectangles in the grid.
If no such configuration exists, return None.
'''
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class Cell:
    def __init__(self, top_left:tuple, width: int, height: int):
        '''
        A cell is represented by its top left corner, width and height.
        
        Cells with width or height == 0 will return None
        '''
        
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
    
    def can_contain(self, c):
        '''
        Returns true if this cell is able to contain the entirety of the input cell.
        '''
        w_check = self.width >= c.width
        h_check = self.height >= c.height
        return w_check and h_check
        
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
    def __init__(self,  width, height, top_left = (-1, -1)):
        '''
        A Rect is a Cell that can't have child Cells.
        The Rect can be moved in its parent Cell.
        '''
        super().__init__(top_left, width, height)
        
    def flip(self):
        '''
        Flips the dimensions of the rectangle
        '''
        self.width, self.height = self.height, self.width
        
    def place(self, coord: tuple):
        '''
        Places the Rect at the given coordinates
        '''
        self.top_left = (coord[0], coord[1])
        
    def __repr__(self):
        return super().__repr__()
    
class Grid:
    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        self.cells: list[Cell] = [Cell((0, 0), n, m)] # Create the main cell
        self.rects: list[Rect] = []
       
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
            if new_cell.area() > 0:
                self.cells.append(new_cell)
    
    def place_rect(self, r: Rect):
        
        for c in self.cells:
            # Iterate over all cells in the grid
            
            if c.can_contain(r):
                # If the rectangle fits in the cell, partition the cell into 4 cells that don't include the rectangle.
                
                r.place(c.top_left) # Place the rectangle at the corner of cell
                self.rects.append(r)
                self.subdivide(c, r) # Subdivide the cell
                
                return True
            
        # Return False since the rect couldn't be placed
        return False
        
    def __repr__(self):
        return self.root.__repr__()
    
    def plot(self):
        #define Matplotlib figure and axis
        fig, ax = plt.subplots()
        ax.plot(self.n + 1,self.m + 1)

        #add rectangles to plot
        for r in self.rects:
            ax.add_patch(Rectangle(r.top_left, r.width, r.height,))

        # Enable grid lines
        ax.grid()

        #display plot
        plt.show()
        
            
    
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

def get_random_config(g: Grid, rects: list[Rect]):
    for r in rects:
        if not g.place_rect(r):
            return False
        
    g.plot()
    return True

g = Grid(10, 10)
rects = [Rect( 5, 5), Rect(2, 3)]
print(get_random_config(g, rects))


