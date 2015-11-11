from world.dynamicObject import DynamicObject

class MovableObject(DynamicObject):
    '''Represents an object that can be moved by the client.'''
    def __init__(self, dim, pos, mass):
        super(DynamicObject, self).__init__(dim, pos, mass)
        return