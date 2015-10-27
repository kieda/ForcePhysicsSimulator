import sys

import problem as p

#import worlds.world1 as w      # 2D test world with a bunch of collision planes

import worlds.world2 as w      # 3D test world
import simulations.sim1 as s   # test simulation .. 10 phases of one timestep each; each timestep is one second;  total 10second simulation
import evaluators.eval1.Evaluator1 as makeEvaluator   # basic evaluator .. penalize dist from goal, deviation from goal velocity, force differences between phases


#---------------------------------------------------------------------------------

# this is here to run a series of tests on the friction code (sliding, sticking, adhere to manifold, etc.)
#import simpleTests.frictionTest as ft

#---------------------------------------------------------------------------------

# do a full CMA optimization defined based on the world, simulation, and evaluator imported above

theWorld = w.makeWorld()
theSim = s.makeSimulation()
theEvaluator = makeEvaluator()

q = p.Problem(theWorld, theSim, theEvaluator)

for i in range(0, 100000):
    q.simulateRandom()

#q.runOptimizer()

#---------------------------------------------------------------------------------

#result = np.linspace(0, -10, 20)

#result = np.zeros(20)

#result = np.empty(20)
#result.fill(-1.05)


#q.simulate(result, True)
#print "evaluates to {}".format(q.evaluate(result))


