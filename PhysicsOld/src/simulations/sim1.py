
import simulation as si

def makeSimulation():
    sim = si.Simulation()
    sim.setNumPhases(10)
    sim.setTimestepsPerPhase(1)
    sim.setTimestep(1)
    sim.setIntegrator(si.Integrator.QuadraticExact)
    return sim
