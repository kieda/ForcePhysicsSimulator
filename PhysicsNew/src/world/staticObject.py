from world.worldObject import WorldObject

class StaticObject(WorldObject):
    ''' 
    represents an object that cannot move. 
    Massless.
    '''
    def __init__(self, dim, pos):
        super(WorldObject, self).__init__(dim, pos)
    
    