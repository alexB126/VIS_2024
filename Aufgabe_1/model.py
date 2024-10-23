import numpy as np

class Model:
    def __init__(self, iniState):
        self.state = iniState

    def get_state(self):
        return self.state
    
    def set_state(self, new_state):
        self.state = new_state

    def dydt(self, t, y):
        """Defines the system's dynamics: computes the derivative of the state vector."""
        raise NotImplementedError("This method should be implemented by subclasses.")


class SingleMassOscillator(Model):
    def __init__(self, iniState, m, k, d):

        # call parent constructor
        super().__init__(iniState)
        #your implementation here

        # set class variables
        self.m = m
        self.k = k
        self.d = d


    def dydt(self, t):
        """Compute the derivatives of the state (velocity and acceleration)."""
        #----------------------------------------------------------------------------
        #  | implementation here  |
        # \ /                    \ /
        #  v                      v
        position = 0.
        velocity = 0.
        acceleration = 0.        
        
        return np.array([velocity, acceleration]) 
        #----------------------------------------------------------------------------

