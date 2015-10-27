import sys
import numpy as np

class Event:
    CollisionType, ZeroVelocityType, BoundaryCrossingType = range(3)



class Collision:    
    def __init__(self, timeIn, pointIn, manifoldIn):
        self.type = Event.CollisionType
        self.time = timeIn
        self.point = pointIn
        self.manifold = manifoldIn


class BoundaryCrossing:    
    def __init__(self, timeIn, pointIn, manifoldIn):
        self.type = Event.BoundaryCrossingType
        self.time = timeIn
        self.point = pointIn
        self.manifold = manifoldIn

        if (timeIn < 0):
            print "BoundaryCrossing requested at a negative time"
            print timeIn
            print pointIn
            print manifoldIn.normal
            print manifoldIn.offset
            sys.exit([0])


# velocity will be zeroed in a certain direction only
#  (first orthogonal to the driving force, and then in the direction of it)
class ZeroVelocity:    
    def __init__(self, timeIn, directionIn):
        self.type = Event.ZeroVelocityType
        self.time = timeIn
        self.direction = directionIn


        
        
