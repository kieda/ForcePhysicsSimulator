import sys

import numpy as np
import matplotlib.pyplot as plt

import event

class Integrator:
    Euler, QuadraticExact = range(2)


class Simulation:
    def __init__(self):
        self.numPhases = 0
        self.integrator = Integrator.Euler

    def setNumPhases(self, phasesIn):
        self.numPhases = phasesIn

    def setTimestepsPerPhase(self, timestepsIn):
        self.timestepsPerPhase = timestepsIn

    def setTimestep(self, timestepIn):
        self.timestep = timestepIn

    def setIntegrator(self, integratorIn):
        self.integrator = integratorIn


    # this function returns the force which will be used to accelerate the particle
    #   .. if we want force that will be applied to a moveable object, we must use the original
    def adjustToManifolds(self, p, forceIn, collisionEpsilon, velocityEpsilon):

        # first, we will check the particle's position and velocity relative to the manifolds .. there are 4 cases:
        #   (1) we have left the manifold (dist > collisionEpsilon)  -->  remove the manifold from the particle's list
        #   (2) we are leaving the manifold (vel > velocityEpsilon)  -->  remove the manifold from the particle's list
        #   (3) we have penetrated the manifold (dist < 0) --> reset to manifold, exiting if (-dist > collisionEpsilon)
        #   (4) we are about to penetrate the manifold (vel < 0) --> reset normal velocity to zero, exiting if (-vel > velocityEpsilon)
        
        removeList = []
        for manifold in p.collisionManifolds:
            normalDist = manifold.distanceFromManifold(p.position)
            normalVelocity = np.dot(p.velocity, manifold.getUnitNormal())

            # check case (1) and (2), we have left or are leaving the manifold
            if (normalDist > collisionEpsilon) or (normalVelocity > velocityEpsilon):
                removeList.append(manifold)

            # check case (3) we have penetrated the manifold
            if (normalDist < 0):
                assert(-1.0*normalDist < collisionEpsilon)     # too much penetration --> exit
                p.position = manifold.projectToManifold(p.position)

            # check case (4)
            if (normalVelocity < 0):
                unitNormal = manifold.getUnitNormal()
                print "we have velocity {} into manifold normal {} at point {}".format(p.velocity, unitNormal, p.position)
                assert ((-1.0*normalVelocity) < velocityEpsilon)    # too much velocity into manifold --> exit
                p.velocity -= np.dot(p.velocity, unitNormal) * unitNormal

        # remove those manifolds we have left or are leaving
        for removable in removeList:
            p.removeCollisionManifold(removable)

        # if we have no manifolds, just return the force that came in
        if len(p.collisionManifolds) == 0:
            return forceIn

        # now we know there is at least one manifold

        # go through all the manifolds collecting 
        #    normalForce --> all force that is in the *positive* normal direction for some manifold
        #                      .. we will use this to determine the size of any frictional force in the case of sliding
        #    tangentForce --> all force remaining once the positive normal forces have been subtracted out
        #                      .. we will test tangentForce/NormalForce vs. mu to determine whether the contact is sticking or sliding
        #                      .. if we have a sticking contact, we return zeros, because there is no force left to accelerate the object
        #    tangentVelocity --> all velocity that is truly tangent to at least one manifold
        #                      .. we use this to determine the size of resistive frictional force added in the case of sliding
        #
        # for coefficient of friction, at the moment we keep the largest coefficient of friction observed .. which is not be exactly right

        remainingForce = np.copy(forceIn)           # start tangent force as force that came in .. we'll subtract off normal forces
        normalForce = np.zeros(len(forceIn))        # start normal force as zero .. we'll add to it from there
        tangentVelocity = np.zeros(len(p.velocity)) # start tangent velocity as zero .. we'll add to it
        remainingVelocity = np.copy(p.velocity)     # we need to track remaining velocity that has not yet been classified as tangent
        mu = 0.0                                    # we will keep the largest coefficient of friction .. initialize to zero

        for manifold in p.collisionManifolds:
            # get the components of force and velocity in this manifold's normal direction
            unitNormal = manifold.getUnitNormal()
            forceDot = np.dot(remainingForce, unitNormal)
            velDot = np.dot(remainingVelocity, unitNormal)

            # only concern ourselves with forces, friction, and velocity if the force is pointing into this manifold
            if forceDot < 0:

                # update normal and tangent forces by adding to the normal force and subtracting the same amount from tangentForce
                addToNormalForce = forceDot * unitNormal
                normalForce += addToNormalForce
                remainingForce -= addToNormalForce

                # update tangent and remaining velocities by adding to the tangentVelocity and subtracting the same from remainingVelocity
                addToTangentVel = remainingVelocity - velDot * unitNormal
                tangentVelocity += addToTangentVel
                remainingVelocity -= addToTangentVel

                # update the coefficient of friction if we have found one that is larger
                manifoldMu = manifold.getCoefficientOfFriction()
                if manifoldMu > mu:
                    mu = manifoldMu


        # collect resultant tangent and normal quantities
        tangentForce = remainingForce
        tangentForceMagnitude = np.linalg.norm(tangentForce)
        normalForceMagnitude = np.linalg.norm(normalForce)
        tangentVelocityMagnitude = np.linalg.norm(tangentVelocity)
        
        # CASE 1:   THERE IS EXISTING TANGENT VELOCITY
        # if there is tangent velocity, there is a resistive force supplied by the object that is at the edge of the friction cone
        # this opposing force will be added to the force used to accelerate / decelerate the particle
        if (tangentVelocityMagnitude > velocityEpsilon):
            unitTangentVelocity = tangentVelocity / tangentVelocityMagnitude
            tangentForce -= mu*normalForceMagnitude*unitTangentVelocity
            return tangentForce

        # we are assumuing zero velocity now, so let's make it so .. 
        #  .. otherwise we are in trouble, because we have not supplied a resistive force to stop it
        p.velocity = np.zeros(len(p.velocity))

        # CASE 2:  THE CONTACT IS STICKING AND WILL REMAIN STICKING DUE TO FORCES WITHIN THE FRICTION CONE
        # if the force is within the friction cone, we can return zero .. there will be no acceleration
        if (tangentForceMagnitude < (mu*normalForceMagnitude)):
            return np.zeros(len(forceIn))

        # CASE 3:  THE CONTACT IS STICKING, BUT WILL BEGIN TO ACCELERATE DUE TO FORCES OUTSIDE THE FRICTION CONE
        # we want to accelerate the particle with whatever force is left that is in excess of the friction cone force
        unitTangentForce = tangentForce / tangentForceMagnitude
        tangentForce -= mu*normalForceMagnitude*unitTangentForce
        return tangentForce



    # advance time assuming freespace motion
    # we assume here that the given force includes gravity and all other forces
    # we also assume it has been adjusted to match the current collision manifolds

    def freeAdvance(self, p, force, timeToGo):
        
        # advance based on this computed force
        if (self.integrator == Integrator.Euler):
            p.position = p.position + p.velocity*timeToGo
            p.velocity = p.velocity + force*timeToGo

        elif (self.integrator == Integrator.QuadraticExact):
            p.position = p.position + p.velocity*timeToGo + (0.5*timeToGo*timeToGo)*force
            p.velocity = p.velocity + force*timeToGo

        else:
            print "Integrator {} not found".format(self.integrator)
            sys.exit([0])


    # following the goal of dissipating energy maximally, we ..
    #   .. clear all velocity that is in the bounds of the friction cone
    def processImpact(self, p, force, collision, velocityEpsilon):

        # get parameters of collision surface
        mu = collision.manifold.getCoefficientOfFriction()
        unitNormal = collision.manifold.getUnitNormal()

        # get the normal part of the velocity
        normalVelocityDotProduct = np.dot(p.velocity, unitNormal)
        normalVelocityMagnitude = np.fabs(normalVelocityDotProduct)
        normalVelocity =  normalVelocityDotProduct * unitNormal

        # get the tangent part of the velocity
        tangentVelocity = p.velocity - normalVelocity
        tangentVelocityMagnitude = np.linalg.norm(tangentVelocity)

        # what we do depends on the velocity direction..
        
        # first, make sure velocity is not going out of the manifold
        assert(normalVelocityDotProduct <= 0)

        if (tangentVelocityMagnitude < velocityEpsilon) or (tangentVelocityMagnitude < (mu*normalVelocityMagnitude)):
            # velocity is inside the friction cone or else the tangent is very small, and we can stop it all
            p.velocity[:] = 0

        else:
            # velocity is not completely inside the friction cone
            # we clear as much of the incoming velocity as the friction cone allows

            # clear normal component
            p.velocity -= normalVelocity

            # clear tangent component as far as friction cone will allow
            unitTangent = tangentVelocity / tangentVelocityMagnitude
            tangentVelocityRemoved = mu * normalVelocityMagnitude * unitTangent
            p.velocity -= tangentVelocityRemoved



    def collideWithPlane(self, collisionPlane, p, force, collisionEpsilon, forceEpsilon):

        if self.integrator == Integrator.Euler:
            return collisionPlane.findCollisionLinear(p.position, p.velocity, collisionEpsilon)

        elif self.integrator == Integrator.QuadraticExact:
            return collisionPlane.findCollisionQuadratic(p.position, p.velocity, force, collisionEpsilon, forceEpsilon)

        else:
            print "Integrator {} not found".format(self.integrator)
            sys.exit([0])


    # here, we just loop through all the collision planes we are not on already, check for collision times,
    #  .. and return the first
    def getFirstCollision(self, p, force, world):

        firstCollision = None

        # try all collision planes we are not already on
        for cp in world.collisionPlanes:
            if (not p.onManifold(cp)):
                collision = self.collideWithPlane(cp, p, force, world.collisionEpsilon, world.forceEpsilon)

                if collision is not None:
                    if (firstCollision is None) or (collision.time < firstCollision.time):
                        firstCollision = collision

        return firstCollision


    def getFirstBoundaryCrossingOnManifold(self, collisionPlane, p, force, world):

        if self.integrator == Integrator.Euler:
            return collisionPlane.getFirstBoundaryCrossingLinear(p.position, p.velocity, world.collisionEpsilon)

        elif self.integrator == Integrator.QuadraticExact:
            return collisionPlane.getFirstBoundaryCrossingQuadratic(p.position, p.velocity, force, world.collisionEpsilon, world.forceEpsilon)
                                                                    
        else:
            print "Integrator {} not found".format(self.integrator)
            sys.exit([0])


    # here, we just loop through all the collision planes we are currently sitting on, 
    #  .. get the first boundary crossing for each of these
    #  .. and return the first from all this set
    def getFirstBoundaryCrossing(self, p, force, world):

        firstBoundaryCrossing = None

        # try all collision planes we are currently sitting on 

        for cp in world.collisionPlanes:
            if (p.onManifold(cp)):
                firstCrossingThisManifold = self.getFirstBoundaryCrossingOnManifold(cp, p, force, world)
                if firstCrossingThisManifold is not None:
                    if (firstBoundaryCrossing is None) or (firstCrossingThisManifold.time < firstBoundaryCrossing.time):
                        firstBoundaryCrossing = firstCrossingThisManifold

        return firstBoundaryCrossing


    # the overall idea when collecting these events is that we are assuming constant force phases ..
    #    .. force is assumed to be constant until the next event, which allows easy calculation of event timelines
    #
    # HOWEVER .. when we are sliding, force may not be constant 
    #    .. the problem -- resistive frictional force lies on the outer boundary of the friction cone opposing the velocity
    #    .. integrated over time, this force may change the velocity direction, thus changing the force direction within the phase
    #
    # To solve this problem, we assume that it is unnatural to experience extended velocities that are orthogonal
    #   to the force direction .. we zero those orthogonal velocities first, and then everything else will happen
    #   along the constant line of the driving force, allowing a constant force relative to the manifold until an event occurs
    #
    # for inputs:
    #  force has been adjusted to all manifolds
    #  unadjustedForce is the original force declared for this timestep
    #
    def getFirstVelocityZero(self, p, force, unadjustedForceIn, world):

        # if we are not on a manifold, we are done
        if not p.onSomeManifold():
            return None

        # if we are not moving, we are done
        if not ((np.linalg.norm(p.velocity) > world.velocityEpsilon)):
            return None

        # if the force coming in is identical to unadjustedForceIn, then the manifolds are having no effect .. we are done
        forceDiff = force - unadjustedForceIn
        if (np.linalg.norm(forceDiff) < world.forceEpsilon):
            return None

        # now, we need to clamp the unadjustedForceIn to the manifolds
        unadjustedForce = p.clampToManifolds(unadjustedForceIn)

        # if the force coming in is identical to the unadjustedForce, then friction is having no effect .. we are done
        forceDiff = force - unadjustedForce
        if (np.linalg.norm(forceDiff) < world.forceEpsilon):
            return None

        # if there is no unadjustedForce (i.e., the driving force), 
        #   .. we have a simple case where friction stops the velocity
        unadjustedForceNorm = np.linalg.norm(unadjustedForce)
        if (unadjustedForceNorm < world.forceEpsilon):

            # there should be some frictional force
            forceMagnitude = np.linalg.norm(force)
            assert (forceMagnitude > 0)
            unitForce = force / forceMagnitude

            # get the velocity in this direction, which should be negative
            velDotForce = np.dot(p.velocity, unitForce)
            if (velDotForce >= 0):
                print "there is no velocity in force direction"
                print p.position
                print p.velocity
                print force
                print unadjustedForceIn
                print unadjustedForce

            assert (velDotForce < 0)

            # time is just velocity / force for these unit mass particles
            zeroTime = -1.0 * velDotForce / forceMagnitude
            return event.ZeroVelocity(zeroTime, unitForce)

        # overall plan in the case of a driving force:   
        #    (1) stop velocity orthogonal to that force
        #    (2) stop velocity in the direction of the force (assuming it opposes the velocity overall)
            
        # find velocity components in the unadjustedForce direction and orthogonal to it
        unitUnForce = unadjustedForce / unadjustedForceNorm
        velInUnForceDirection = np.dot(p.velocity, unitUnForce) * unitUnForce
        orthogonalVelocity = p.velocity - velInUnForceDirection
        orthogonalVelocityNorm = np.linalg.norm(orthogonalVelocity)

        # find force components in the unadjustedForce direction and orthogonal to it
        forceInUnForceDirection = np.dot(force, unitUnForce) * unitUnForce
        orthogonalForce = force - forceInUnForceDirection
        orthogonalForceNorm = np.linalg.norm(orthogonalForce)

        # if there is some orthogonalVelocity, we'll zero this first
        if (orthogonalVelocityNorm > world.velocityEpsilon):

            # force should oppose the velocity, because it should just be frictional
            assert(np.dot(orthogonalVelocity, orthogonalForce) < 0)

            # time is just velocity / force for these unit mass particles
            zeroTime = orthogonalVelocityNorm / orthogonalForceNorm
            return event.ZeroVelocity(zeroTime, orthogonalForce / orthogonalForceNorm)

        # there is no orthogonal velocity ..
        # if the velocity in the driving force direction does not oppose the cumulative force, we're done
        velDotForce = np.dot(forceInUnForceDirection, velInUnForceDirection)
        if (velDotForce > 0):
            return None
          
        # force in the driving force direction does oppose velocity .. zero this opposing velocity
        # time is just velocity / force for these unit mass particles
        forceInUnForceDirectionNorm = np.linalg.norm(forceInUnForceDirection)
        zeroTime = np.linalg.norm(velInUnForceDirection) / forceInUnForceDirectionNorm
        return event.ZeroVelocity(zeroTime, forceInUnForceDirection / forceInUnForceDirectionNorm)



    # at the moment, the only kinds of events we know about that require recomputing forces are:
    #    . the particle may collide with something else in the world
    #    . if the particle is sliding on a manifold, its velocity may go to zero
    #
    def getNextEvent(self, p, force, unadjustedForce, world):

        firstEvent = None

        # get time to first collision
        firstCollision = self.getFirstCollision(p, force, world)
        if (firstCollision is not None):
            firstEvent = firstCollision

        # get time to velocity zero
        firstVelocityZero = self.getFirstVelocityZero(p, force, unadjustedForce, world)
        if (firstVelocityZero is not None):
            if (firstEvent is None) or (firstVelocityZero.time < firstEvent.time):
                firstEvent = firstVelocityZero

        # if we are on any manifolds, get the first time to cross a boundary
        firstBoundaryCrossing = self.getFirstBoundaryCrossing(p, force, world)
        if (firstBoundaryCrossing is not None):
            if (firstEvent is None) or (firstBoundaryCrossing.time < firstEvent.time):
                firstEvent = firstBoundaryCrossing

        return firstEvent


    def printEvent(self, e, p, timeToGo):
        if e is None:
            print "no event .. free simulation for time {}".format(timeToGo)

        elif e.type == event.Event.CollisionType:
            print "collision at time {} at point {} on manifold with normal {}".format(e.time, e.point, e.manifold.normal)

        elif e.type == event.Event.BoundaryCrossingType:
            print "boundary crossing at time {} at point {} from manifold with normal {}".format(e.time, e.point, e.manifold.normal)

        elif e.type == event.Event.ZeroVelocityType:
            print "hitting zero velocity at time {}".format(e.time)

        else:
            print "did not recognize event"


    # sanity check .. did the integrator take us where the event detector expected?
    def checkPosition(self, pos, expectedPos, collisionEpsilon):
        posDiff = np.linalg.norm(pos - expectedPos)
        if (posDiff > collisionEpsilon):
            print "pos {} .. expected {}".format(pos, expectedPos)
            return False   # for debugging
        assert(posDiff < collisionEpsilon)
        return True   # for debugging
        
    # sanity check .. did the integrator take us where the zero velocity calculation predicted?
    def checkVelocityZero(self, vel, direction, velocityEpsilon):
        velDotDirection = np.dot(vel, direction)
        if (velDotDirection > velocityEpsilon):
            print "expected zero velocity in direction {} got {} .. velocity is {}".format(direction, velDotDirection, vel)
        #assert(velDotDirection < velocityEpsilon)

    # sanity check .. did the integrator give us a result where we have significant velocity *into* a contact surface?
    def checkVelocityAgainstManifolds(self, p, force, velocityEpsilon):
        # loop over manifolds
        for manifold in p.collisionManifolds:
            velAgainstNormal = -1.0*np.dot(p.velocity, manifold.getUnitNormal())
            if (velAgainstNormal >= velocityEpsilon):
                print "position {} velocity {} manifold normal {} force {}".format(p.position, p.velocity, manifold.getUnitNormal(), force)
            assert (velAgainstNormal < velocityEpsilon)


    # the goal of this function is to eventually advance the given particle an entire timestep
    # in practice, it will: 
    #        . advance the particle to the next event, 
    #        . process that event, and 
    #        . spawn a recursive call to complete the timestep
    #
    def advanceActiveObject(self, p, forceIn, timeToGo, world, count):

        # stop infinite recursion
        if count > 10:
            print "called advanceActiveObject 10 times and we still have {} time to go".format(timeToGo)
            sys.exit([0])

        # if the particle is already on any manifolds, we need to adjust the force to match those manifolds
        force = self.adjustToManifolds(p, forceIn, world.collisionEpsilon, world.velocityEpsilon)

        # get the time to the next event
        nextEvent = self.getNextEvent(p, force, forceIn, world)

        # branch depending on whether there is an event within our timestep
        if (nextEvent is None) or (nextEvent.time >= timeToGo):
            # nothing to worry about now, just freeAdvance
            self.checkVelocityAgainstManifolds(p, force, world.velocityEpsilon)          # CHECK: no velocity into manifold before advance
            self.freeAdvance(p, force, timeToGo)
            self.checkVelocityAgainstManifolds(p, force, world.velocityEpsilon)          # CHECK: no velocity into manifold after advance
            #print "no event before our time is up .. free simulation for time {}".format(timeToGo)

        else:
            #self.printEvent(nextEvent, p, timeToGo)

            # for debugging
            startPosition = p.position
            startVelocity = p.velocity

            # freeAdvance as far as we can go
            self.checkVelocityAgainstManifolds(p, force, world.velocityEpsilon)          # CHECK: no velocity into manifold before advance
            self.freeAdvance(p, force, nextEvent.time)
            self.checkVelocityAgainstManifolds(p, force, world.velocityEpsilon)          # CHECK: no velocity into manifold after advance

            # if we have a collision, process the collision and add the new manifold
            if nextEvent.type == event.Event.CollisionType:
                #self.checkPosition(p.position, nextEvent.point, world.collisionEpsilon)  # CHECK: reached calculated collision point

                if (not self.checkPosition(p.position, nextEvent.point, world.collisionEpsilon)):
                    print "position {} velocity {} force {}  forceIn {}".format(startPosition, startVelocity, force, forceIn)
                    sys.exit([0])

                self.processImpact(p, force, nextEvent, world.velocityEpsilon)
                self.checkVelocityAgainstManifolds(p, force, world.velocityEpsilon)      # CHECK: no velocity into manifold after impact
                p.addCollisionManifold(nextEvent.manifold)

            # if we have a boundary crossing, process the boundary crossing .. we are leaving the manifold
            if nextEvent.type == event.Event.BoundaryCrossingType:
                self.checkPosition(p.position, nextEvent.point, world.collisionEpsilon)  # CHECK: reached expected crossing point
                p.removeCollisionManifold(nextEvent.manifold)

            if nextEvent.type == event.Event.ZeroVelocityType:
                self.checkVelocityZero(p.velocity, nextEvent.direction, world.velocityEpsilon)  # CHECK: velocity has in fact gone to zero

            # advance the rest of the timestep .. 
            # .. passing in the ORIGINAL force so that it can be adjusted properly from scratch
            self.advanceActiveObject(p, forceIn, (timeToGo-nextEvent.time), world, count+1)



    def simulate(self, world, forceInfo, saveResults=False):

        # put the world back to its initial state
        world.setToInitialState()

        # we'll need these variables handy
        numActiveObjects = world.getNumberOfActiveObjects()
        numDimensions = world.numDimensions

        # if we're saving results, initialize the array to hold them
        if (saveResults):
            # the results array will be ( activeObjects X phases*tsPerPhase )
            res = np.zeros((numActiveObjects, self.numPhases*self.timestepsPerPhase, numDimensions))
            velRes = np.zeros((numActiveObjects, self.numPhases*self.timestepsPerPhase, numDimensions))
            forceRes = np.zeros((numActiveObjects, self.numPhases*self.timestepsPerPhase, numDimensions))
            resCount = 0

        # loop through every timestep in every phase, advancing time ...
        for phase in range(0, self.numPhases):
            for ts in range(0, self.timestepsPerPhase):

                # advance active objects one at a time, as if they are independent
                #  .. this is obviously not a long term solution
                for pIndex in range(numActiveObjects):

                    # get the current object to advance
                    p = world.getActiveObject(pIndex)

                    # the world knows how to unpack the force from the flat forceInfo vector
                    #   .. it also adds gravity, etc ..
                    #   .. we have a built-in assumption here that force is constant over the timestep
                    force = world.getForce(forceInfo, phase, pIndex)

                    # do whatever is needed to advance this object over the entire timestep at this force
                    self.advanceActiveObject(p, force, self.timestep, world, 0)

                    # record the result if desired
                    if (saveResults):
                        res[pIndex, resCount] = p.position
                        velRes[pIndex, resCount] = p.velocity
                        forceRes[pIndex, resCount] = force

                    # check if we have tunneled...
                    if (p.position[1] < 20) and (p.position[0] < 35):
                        # we should not be here ...
                        print "position {}".format(res)
                        print "velocity {}".format(velRes)
                        print "force {}".format(forceRes)
                        sys.exit([0])
                        

                if (saveResults):
                    resCount += 1

                # later, we will advance inactive, but movable objects
                # .. or perhapse we should somehow advance everything together

        if (saveResults):
            #print "position {}".format(res)
            #print "velocity {}".format(velRes)
            #print "force {}".format(forceRes)
            
            plt.scatter(res[0,:,0], res[0,:,1], c=np.random.rand(3,1))
            #plt.scatter(res[0,:,0], res[0,:,2], c=np.random.rand(3,1))

            # call for two particles
            #plt.plot(res[0,:,0], res[0,:,1], 'ro', res[1,:,0], res[1,:,1], 'bs')



