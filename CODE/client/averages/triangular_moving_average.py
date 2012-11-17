from average import Average

class Triangular(Average):
    """
    A smoothed version of the SMA.
    """
    
    def add_successive_points(self, point):
        """
        Formula:
            TMA_t = sum_{i=1}^N SMA_{t-N+1} / N
        """
        
        pass

    def add_initial_points(self, point):
        """
        Formula:
            for some t <= N:
                TMA_t = (SMA_t + SMA_{t-1} + ... + SMA_1) / t
        """

        
