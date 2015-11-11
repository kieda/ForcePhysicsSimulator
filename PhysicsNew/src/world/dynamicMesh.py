from world.dynamicObject import DynamicObject
from world.mesh import Mesh

class DynamicMesh(DynamicObject, Mesh):
    def __init__(self, boundaries, dim, pos, rot, mass):
        '''
        @param boundaries: the boundaries for this dynamic mesh
        @param pos: the initial translation of this mesh
        @param rot: the initial position of this mesh
        @param mass: the mass of this mesh
        '''
        super(DynamicObject, self).__init__(dim, pos, mass)
        super(Mesh, self).__init__(dim, boundaries)
        self.rot = rot.copy()
        
        