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
        self.points.append(point)

        numerator = 0.0
        for i in xrange(1, len(self.points) + 1):
            numerator += simple_moving_average(self.time - self.set_size + i)

        return numerator/self.set_size

    def add_initial_points(self, point):
        """
        Formula:
            for some t <= N:
                TMA_t = (SMA_t + SMA_{t-1} + ... + SMA_1) / t
        """
        self.points.append(point)
        
        numerator = 0.0
        for i in xrange(1, len(self.points) + 1):
            numerator += simple_moving_average(i)
        
        return numerator/len(self.points)

    def simple_moving_average(self, time):
        """
        We re-implement SMA in this method for performance improvements over
        calling the existing SMA class.

        Parameters:
            time -- The time tick that we want to calculate SMA in
        """

        if time < self.set_size:
            return sum(self.points[:time])/time
        else:
            # Performance improvement possible, but probably unnecessary
            return sum(self.points[time - self.set_size : time])/self.set_size
