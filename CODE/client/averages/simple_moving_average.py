from average import Average

class Simple(Average):
    """
    The unweighted mean of the last N data points.
    """
    
    def add_successive_points(self, point):
        """
        Formula:
            SMA_t = SMA_{t-1} - (price_{t-N} / N) + (price_t / N)
        """

        self.average -= (self.points.pop(0)) / self.set_size
        self.average += point / self.set_size

        self.points.append(point)

        return self.average

    def add_initial_points(self, point):
        """
        Formula:
            for some t <= N:
                SMA_t = (price_t + price_{t-1} + ... + price_1) / t
        """

        self.points.append(point)
        self.average = sum(self.points) / len(self.points)

        return self.average
