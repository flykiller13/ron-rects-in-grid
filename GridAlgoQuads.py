import quads
import random

n = 10
m = 10
tree = quads.QuadTree((0, 0), 10, 10)
p = quads.Point(4, 4)
tree.insert(p)
tree._root.subdivide()

quads.visualize(tree, 10)