'''
handle for the controller. Immutable for ease of use to the client.
'''
import copy.copy

class Handle:
    
    def __init__(self):
        self.activeForces = {}
        self.parent = None
        self.children = []
        self.idCount = 0
    
    def _branch(self):
        handle = Handle()
        handle.parent = self
        handle.activeForces = copy(self.activeForces)
        handle.idCount = self.idCount
        self.children.append(handle)
        return handle
        
    def getOtherSteps(self):
        return self.children
    
    def currentState(self):
        return self.state
        
    def stepBack(self):
        return self.parent
    
    def stepForward(self):
        # 1. branch, 2. 
        return self._branch()
        
    def applyActiveForce(self, movableObject, force, phase):
        id = self.idCount
        self.idCount = self.idCount + 1
        
        return self._branch()
    def applyActiveForces(self, movableObject, forces):
        handle = self
        for force, phase in forces:
            handle = handle.applyActiveForce(movableObject, force, phase)
        return handle
    def removeActiveForce(self, id):
        handle = self._branch()
        handle.activeForces.remove(id)
        return handle
        
    def filterActiveForces(self, filterFn):
        handle = self
        for id, force in self.activeForces:
             handle = handle.removeActiveForce(id)
        return handle
    
    def getActiveForceInfo(self, id):
        return self.activeForces[id]
        
    def getActiveForces(self):
        return self.activeForces
    
    def getActiveForcesByObject(self, movableObject):
        return [id for id, force in self.activeForces if movableObject is force.movableObject]
    
    
        
# todo : have progress measure that can track how close objects are to their goal.
# (movableObject, finalTransform, finalVelocity) -> double

# possible : have "distance function" such that
# distance :  (finalTransform, finalVelocity) ->  (movableObject) ->  double

# then the progress is defined as 
'''
    progress = let
        dist = distance(finalTransform, finalVelocity)
    in dist(currentObject) / dist(originalObject)
    end 
'''  
# then, the progress is based on the ratio of the current distance and the original distance.
# in the case that the original distance is near zero, we can accept the original state as the final state. 
# Note that originally progress = 1.0, and the evaluator works to make it drop to values below 1.0. 
# we automatically know that if the progress exceeds 1.0, then the evaluator is making the object
# go further from the goal than we originally started.