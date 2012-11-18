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
        
        numerator, denominator = 0.0, 0.0
        self.points.append(point)

        for i in xrange(self.set_size):
            numerator += self.points[i + 1] * (i + 1)
            denominator += (i + 1)

        return numerator/denominator

    def add_initial_points(self, point):
        """
        Formula:
            for some t <= N:
                LWMA_t = (price_t * t) + ... + (price_1 * 1) / sum_{i=1}^t i
        """

        self.points.append(point)
        numerator, denominator = 0.0, 0.0

        for i in xrange(len(self.points)):
            numerator += self.points[i] * (i + 1)
            denominator += (i + 1)

        return numerator/denominator
