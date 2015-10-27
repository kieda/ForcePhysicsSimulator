import abc

class WorldObject(object):
    
    def __init__(self):
    
    @abc.abstractmethod
    def testCollision(self, other):    
        