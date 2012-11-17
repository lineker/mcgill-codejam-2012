from average import Average

class Exponential(Average):
    """
    Similar to the LWMA, but applies exponentially decreasing weighting factors
    to the data points, giving more importance to the latest data points.
    """

    def add_successive_points(self, point):
        """
        Formula:
            EMA_t = EMA_{t-1} + a * (price_t - EMA_{t-1})
                where a = 2 / (N+1)
        """

        self.points.append(point)
        a = 2 / (self.set_size + 1)
        self.average = self.average + a * (point - self.average)

        return self.average

    def add_initial_points(self, point):
        """
        Because N and t are not dependent on each other in this formula,
        we can let EMA_1 = price_1, then use the formula for all t > 1.
        """
        if self.time == 0:
            return point
        else:
            return add_successive_points(point)
