'''
note: previously named "evaluator". Controller is more general, since the client might
not write an evaluator for their simulation, they're just writing a method to control
the system.

We provide an evaluator controller, however, as a basic method for clients to use.
'''
from abc import abstractmethod

class Controller:
    @abstractmethod
    def run(self, handle):
        ''' Note: (very non-python like and maybe a bit too much like java...)
        A client should implement the controller as a subclass.  
        '''
        
        
    
        