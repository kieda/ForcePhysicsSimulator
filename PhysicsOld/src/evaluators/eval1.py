import evaluator as e
from __builtin__ import True

'''
def makeEvaluator():
    eval = e.Evaluator()
    eval.doSqrDistFromGoal = True
    eval.doSqrVelocityError = True
    eval.doSqrForceDiffs = True
    return eval
'''

class Evaluator1 (e):
    def __init__(self):
        self.doSqrDistFromGoal = True
        self.doSqrVelocityError = True
        self.doSqrForceDiffs = True
        