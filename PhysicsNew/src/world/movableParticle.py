from world.movableObject import MovableObject
from world.particle import Particle

class MovableParticle(MovableObject, Particle):
    def __init__(self, params):
        return