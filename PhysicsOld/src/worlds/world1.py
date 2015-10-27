import worldObjects as wo
import numpy as np



def makeCollisionSegment2D(p1, p2, mu):

    # unit normal is z X (p2-p1) .. divided by its magnitude
    pointDiff = p2 - p1
    scaledNormal = np.array([-1.0*pointDiff[1], pointDiff[0]])
    scaledNormalMag = np.linalg.norm(scaledNormal)
    assert(scaledNormalMag > 0)   # the points should not be identical...
    normal = scaledNormal / scaledNormalMag

    # offset is either of the points dotted with the unit normal
    offset = np.dot(p1, normal)

    # make the collision plane
    cp = wo.CollisionPlane(normal, offset, mu)

    # make and add the boundary corresponding to p1
    direction1 = -1.0*pointDiff / np.linalg.norm(pointDiff)
    boundary = wo.CollisionPlaneBoundary(p1, direction1, 0.0, cp)
    cp.addBoundary(boundary)

    # make and add the boundary corresponding to p2
    direction2 = -1.0*direction1
    boundary = wo.CollisionPlaneBoundary(p2, direction2, 0.0, cp)
    cp.addBoundary(boundary)    

    return cp


def addBox2D(world, xmin, xmax, ymin, ymax, mu):
    pointList = []
    pointList.append(np.array([xmin, ymin]))
    pointList.append(np.array([xmin, ymax]))
    pointList.append(np.array([xmax, ymax]))
    pointList.append(np.array([xmax, ymin]))
    addPolygon2D(world, pointList, mu)


# a polygon in 2D is just a collection of collision planes with their boundaries
#  .. this method expects points in *clockwise* direction
def addPolygon2D(world, pointList, mu):

    # there should be at least two points .. we'll do squished polys, but not a single point
    assert(len(pointList) > 1)

    # loop through the points, creating segments and adding them to the world
    firstPoint = pointList[-1]
    for secondPoint in pointList:
        # make a segment from firstPoint to secondPoint and add it to the world
        segment = makeCollisionSegment2D(firstPoint, secondPoint, mu)
        world.addCollisionPlane(segment)

        # update the firstPoint for the next iteration
        firstPoint = secondPoint
    



def makeWorld():

    # create a world
    world = wo.World()

    # 2 dimensions
    world.numDimensions = 2

    # regular gravity
    world.gravity = np.array([0.0, -9.8])

    # add a particle
    startPos = np.array([20.,100.])
    startVel = np.array([0.,0.])
    
    goalPos = np.array([0.,20.])
    goalVel = np.array([0.,0.])

    p = wo.Particle(startPos, startVel, goalPos, goalVel)
    world.addParticle(p)

    # set coefficient of friction
    mu = 1.

    # add a horizontal collision plane
    normal = np.array([0., 1.])
    offset = 20.
    cp = wo.CollisionPlane(normal, offset, mu)

    # the plane extends only to the left of x=35
    pointOnPlane = np.array([35., 20.])
    direction = np.array([1., 0])
    boundary = wo.CollisionPlaneBoundary(pointOnPlane, direction, 0.0, cp)
    cp.addBoundary(boundary)

    world.addCollisionPlane(cp)

    # close off the "cliff" created by this gap
    normal = np.array([1., 0.])
    offset = 35.
    cp = wo.CollisionPlane(normal, offset, mu)

    # the plane extends only below x=20
    pointOnPlane = np.array([35., 20.])
    direction = np.array([0., 1.0])
    boundary = wo.CollisionPlaneBoundary(pointOnPlane, direction, 0.0, cp)
    cp.addBoundary(boundary)

    world.addCollisionPlane(cp)

    # add a vertical collision plane
    normal = np.array([-1., 0.])
    offset = -40.
    cp = wo.CollisionPlane(normal, offset, mu)
    world.addCollisionPlane(cp)

    # make a box in the middle of the world
    addBox2D(world, -20, 20, 40, 60, mu)

    return world
