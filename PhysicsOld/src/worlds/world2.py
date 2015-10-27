import worldObjects as wo
import numpy as np



def makeWorld():

    # create a world
    world = wo.World()

    # 3 dimensions
    world.numDimensions = 3

    # regular gravity
    world.gravity = np.array([0.0, -9.8, 0.0])

    # add a particle
    startPos = np.array([20.,100., 0.0])
    startVel = np.array([0.,0.,0.])
    
    goalPos = np.array([0.,20.,50.])
    goalVel = np.array([0.,0.,0.])

    p = wo.Particle(startPos, startVel, goalPos, goalVel)
    world.addParticle(p)

    # set coefficient of friction
    mu = 0.1

    # add a horizontal collision plane
    normal = np.array([0., 1., 0.])
    offset = 20.
    cp = wo.CollisionPlane(normal, offset, mu)

    # the plane extends only to the left of x=35
    pointOnPlane = np.array([35., 20., 0.])
    direction = np.array([1., 0., 0.])
    boundary = wo.CollisionPlaneBoundary(pointOnPlane, direction, 0.0, cp)
    cp.addBoundary(boundary)

    world.addCollisionPlane(cp)

    # close off the "cliff" created by this gap
    normal = np.array([1., 0., 0.])
    offset = 35.
    cp = wo.CollisionPlane(normal, offset, mu)

    # the plane extends only below x=20
    pointOnPlane = np.array([35., 20., 0.])
    direction = np.array([0., 1.0, 0.])
    boundary = wo.CollisionPlaneBoundary(pointOnPlane, direction, 0.0, cp)
    cp.addBoundary(boundary)

    world.addCollisionPlane(cp)

    # add a vertical collision plane
    normal = np.array([-1., 0., 0.])
    offset = -40.
    cp = wo.CollisionPlane(normal, offset, mu)
    world.addCollisionPlane(cp)



    return world
