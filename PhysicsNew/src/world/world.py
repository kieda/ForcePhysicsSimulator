from world.dynamicObject import DynamicObject
from world.worldObject import WorldObject

class World:
    def __init__(self, dim):
        self.dim = dim
        self.worldObjects = []
        self.dynamicObjects = []
        return
    
    def addWorldObject(self, worldObject):
        if not isinstance(WorldObject, worldObject):
            raise TypeError("Attempt to add a non-dynamic object as a DynamicObject!")
        
        assert worldObject.dim == self.dim, "Incorrect dimension for worldObject %r" % worldObject
        self.worldObjects.append(worldObject)
    
    def addDynamicObject(self, dynamicObject):
        if not isinstance(DynamicObject, dynamicObject):
            raise TypeError("Attempt to add a non-dynamic object as a DynamicObject!")
        self.addWorldObject(dynamicObject)
        self.dynamicObjects.append(dynamicObject)
    
    