from abc import abstractmethod
import numpy

class WorldObject(object):
    
    def __init__(self, dim, pos):
        ''' 
        @param dim: the number of dimensions that we are using. Currently we only support 2d and 3d
        @param pos: 2d or 3d vector that represents the position of the object.
        ''' 
        if dim not in [2, 3]:
            raise ValueError("Invalid dimension value \"" + dim + "\", only 2 or 3 allowed.")
        
        if not isinstance(pos, numpy.ndarray):
            raise TypeError("pos should be of type " + type(numpy.ndarray))
        
        if dim != pos.size:
            raise ValueError("Expected pos to have size " + dim + ", instead it has size " + pos.size)
        
        self.pos = pos.copy()
        self.collisions = set()
        return
    
    def addCollision(self, collidingObject):
        ''' 
        @param collidingObject : the object that this worldObject has collided with 
        '''
        self.collisions.add(collidingObject)
    
    def removeCollision(self, collidingObject):
        '''
        @param collidingObject: the object that we will remove as a collision 
        '''
        self.collisions.remove(collidingObject)
    
    
    # *** begin abstract methods ***
    
    @abstractmethod
    def testCollision(self, other):
        '''
        @param other: The other object that we are testing a collision for
        @return True iff the object will collide, along with the change in time that it 
        would take for the collision to occur.  
        '''
        return
    
    @abstractmethod
    def nextEvent(self):
        '''
        @return the next event that is emitted by this worldObject. 
        '''
        return
        