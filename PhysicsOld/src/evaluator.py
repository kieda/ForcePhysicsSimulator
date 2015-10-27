import numpy as np


class Evaluator():
    def __init__(self):
        self.doSqrDistFromGoal = True
        self.doSqrVelocityError = True
        self.doSqrForceDiffs = True


    def evaluate(self, world, numPhases, x):
        err = 0.0
        if (self.doSqrDistFromGoal):
            err += world.sqrDistFromGoal()
        if (self.doSqrVelocityError):
            err += world.sqrVelocityError()
        if (self.doSqrForceDiffs):
            err += world.sqrForceDiffs(x, numPhases)
        return err
