import numpy as np

import problem as p
import worldObjects as wo
import simulation as si
import evaluator as e


# this is a 2D world with regular gravity
# there is one particle
# there is a single horizontal collision plane

def makeWorld():

    # create a world
    world = wo.World()

    # 2 dimensions
    world.numDimensions = 2

    # regular gravity
    world.gravity = np.array([0.0, -9.8])

    # add a particle
    startPos = np.array([20.,100.])
    startVel = np.array([5.,0.])
    
    goalPos = np.array([40.,20.])
    goalVel = np.array([0.,0.])


    p = wo.Particle(startPos, startVel, goalPos, goalVel)
    world.addParticle(p)

    # set coefficient of friction
    mu = 0.2

    # add a horizontal collision plane
    normal = np.array([0., 1.])
    offset = 20.
    cp = wo.CollisionPlane(normal, offset, mu)
    world.addCollisionPlane(cp)

    return world


# just one phase to allow easy setup and computation by hand
# one huge timestep of 10 seconds

def makeSimulation():
    sim = si.Simulation()
    sim.setNumPhases(1)
    sim.setTimestepsPerPhase(10)   # was 1
    sim.setTimestep(1)   # was 10
    sim.setIntegrator(si.Integrator.QuadraticExact)
    return sim


# achieve goal with minimal force

def makeEvaluator():
    eval = e.Evaluator()
    eval.doSqrDistFromGoal = True
    eval.doSqrVelocityError = True
    eval.doSqrForceDiffs = True     # note that force diff includes diff from zero at ends
    return eval


# make a Problem
world = makeWorld()
sim = makeSimulation()
eval = makeEvaluator()
q = p.Problem(world, sim, eval)


# work through all the cases for a single collision plane

# (1) the particle falls and sticks to the surface

q.world.particleList[0].startPosition[0] = 20.
q.world.particleList[0].startPosition[1] = 25.
q.world.particleList[0].startVelocity[0] = 5.
q.world.particleList[0].startVelocity[1] = 0.
q.world.collisionPlanes[0].mu = 0.6
result = np.zeros(2)
print "\nTest 1 (Fall and stick).\nAnswer should be [{} {}]".format(25.05076272, 20.0)
q.simulate(result, True)


# (2) the particle falls and sticks, but then accelerates

q.world.particleList[0].startPosition[0] = 20.
q.world.particleList[0].startPosition[1] = 100.
q.world.particleList[0].startVelocity[0] = -2.
q.world.particleList[0].startVelocity[1] = 0.
q.world.collisionPlanes[0].mu = 0.3
result = np.array([3.2, 0.0])
print "\nTest 2 (Fall, stick, then accelerate).\nAnswer should be [{} {}]".format(42.65809114, 20.0)
q.simulate(result, True)


# (3) the particle falls and slides, slowing to a stop and sticking

q.world.particleList[0].startPosition[0] = 20.
q.world.particleList[0].startPosition[1] = 100.
q.world.particleList[0].startVelocity[0] = 2.
q.world.particleList[0].startVelocity[1] = 0.
q.world.collisionPlanes[0].mu = 0.3
result = np.array([2.6, 0.0])
print "\nTest 3 (Fall, slide, then stick).\nAnswer should be [{} {}]".format(49.88235294, 20.0)
q.simulate(result, True)


# (4) the particle falls and slides, slowing to a stop, reversing direction, and accelerating in that direction

q.world.particleList[0].startPosition[0] = 20.
q.world.particleList[0].startPosition[1] = 100.
q.world.particleList[0].startVelocity[0] = 30.
q.world.particleList[0].startVelocity[1] = 0.
q.world.collisionPlanes[0].mu = 0.3
result = np.array([-3.2, 0.0])
print "\nTest 4 (Fall, slide, stop, reverse direction, accelerate).\nAnswer should be [{} {}]".format(113.8900041, 20.0)
q.simulate(result, True)


# (5) the particle falls and slides, continuing to accelerate

q.world.particleList[0].startPosition[0] = 20.
q.world.particleList[0].startPosition[1] = 100.
q.world.particleList[0].startVelocity[0] = 2.
q.world.particleList[0].startVelocity[1] = 0.
q.world.collisionPlanes[0].mu = 0.3
result = np.array([4.0, 0.0])
print "\nTest 5 (Fall, slide, accelerate).\nAnswer should be [{} {}]".format(117.0, 20.0)
q.simulate(result, True)




