from world.staticObject import StaticObject
from world.mesh import Mesh

class StaticMesh(StaticObject, Mesh):
    def __init__(self, dim, boundaries, pos, rot):
        super(StaticObject, self).__init__(dim, pos)
        super(Mesh, self).__init__(dim, boundaries)
        self.rot = rot
        return