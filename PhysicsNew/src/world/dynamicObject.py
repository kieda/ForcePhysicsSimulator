
from world.worldObject import WorldObject

class DynamicObject(WorldObject):
    def __init__(self, dim, pos, mass):
        super(WorldObject, self).__init__(dim, pos)
        self.mass = mass
        
        
        