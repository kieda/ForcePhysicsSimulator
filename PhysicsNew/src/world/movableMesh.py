from world.movableObject import MovableObject
from world.mesh import Mesh

class MovableMesh(MovableObject, Mesh):

    def __init__(self, boundaries, dim, pos, rot, mass):    
        return