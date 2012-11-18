from average import Average
from averages import Simple

class Triangular(Average):
    """
    A smoothed version of the SMA.
	
    The __init__ method was overrided for creating the attributes below.
    The update method was override for calculating the sma average.

    Attributes
        sma    -- The SMA instance that is used to do the sma calculations
        sma_av -- A list that contains the lastest sma averages (should contain only the last 'set_size' calculations
    """
    
    def __init__(self, set_size):
        super(Triangular, self).__init__(set_size)
        self.sma = Simple(set_size)
        self.sma_av = []

    def update(self, point):
        self.sma_av.append(self.sma.update(point))
        if len(self.sma_av) > self.set_size:
            self.sma_av.pop(0)
    	return super(Triangular, self).update(point)

    def add_successive_points(self, point):
        """
        Formula:
            TMA_t = sum_{i=1}^N SMA_{t-N+i} / N
        """
        self.points.append(point)

        numerator = 0.0
        for i in range(self.set_size):
            numerator += self.sma_av[i]

        return numerator/self.set_size

    def add_initial_points(self, point):
        """
        Formula:
            for some t <= N:
                TMA_t = (SMA_t + SMA_{t-1} + ... + SMA_1) / t
        """
        self.points.append(point)
        
        numerator = 0.0
        for i in xrange(self.time + 1):
            numerator += self.sma_av[i]
        
        return numerator/len(self.points)