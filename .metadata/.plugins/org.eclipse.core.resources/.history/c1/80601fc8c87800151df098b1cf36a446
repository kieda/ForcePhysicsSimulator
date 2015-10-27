import cma
import numpy as np

class Problem:
    def __init__(self, worldIn, simIn, evalIn):

        # the current world -- objects, starting locations, goals
        self.world = worldIn

        # the current simulation environment
        self.sim = simIn

        # an evaluator
        self.eval = evalIn


    def simulate(self, x, doPlot=False):
        self.sim.simulate(self.world, x, doPlot)


    def evaluate(self, x):
        self.simulate(x)
        value = self.eval.evaluate(self.world, self.sim.numPhases, x)
        return value

    def simulateRandom(self):

        # how many variables do we have? .. compute the problem size
        # .. right now, there is a force variable for every active object, for every phase
        numActiveObjects = self.world.getNumberOfActiveObjects()
        numDimensions = self.world.numDimensions
        numPhases = self.sim.numPhases
        problemSize = numPhases * numActiveObjects * numDimensions

        maxScale = 20
        input = np.random.rand(problemSize) * maxScale - maxScale/2

        #print "simulating {}".format(input)
        self.simulate(input, True)


    def runOptimizer(self):

        # how many variables do we have? .. compute the problem size
        # .. right now, there is a force variable for every active object, for every phase
        numActiveObjects = self.world.getNumberOfActiveObjects()
        numDimensions = self.world.numDimensions
        numPhases = self.sim.numPhases
        problemSize = numPhases * numActiveObjects * numDimensions

        # make the CMA object
        # the last argument is a single number indicating the spread within which
        #   we expect to see a solution .. here it is 100
        es = cma.CMAEvolutionStrategy(problemSize*[0], 10.0)

        # run the optimization
        MAX_ITERATIONS = 1000
        es.optimize(self.evaluate, MAX_ITERATIONS)

        # get and print the final result
        print "Final result:  {}".format(es.result()[0])

        # now we can run the simulation again, storing results for rendering / analysis
        self.simulate(es.result()[0], True)

