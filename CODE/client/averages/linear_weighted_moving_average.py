from average import Average

class LinearWeighted(Average):
    """
    Description of this moving average.
    """
    
    def add_successive_points(self, point):
        """
        Formula:
            LWMA_t = sum_{i=1}^N price_{t-N+i} * i / sum_{i=1}^N i
        """
        
        pass

    def add_initial_points(self, point):
        """
        Formula:
            for some t <= N:
                LWMA_t = (price_t * t) + ... + (price_1 * 1) / sum_{i=1}^t i
        """

        pass
