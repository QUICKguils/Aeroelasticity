import numpy as np

def compute_reduced_velocity(speed_flow, diameter, frequency) :
    """
    Compute the reduced velocity
    """
    return speed_flow  / frequency /diameter
def compute_mass_ratio(mass_structure, mass_fluid) :
    """
    Compute the mass ratio
    """
    return mass_structure / mass_fluid