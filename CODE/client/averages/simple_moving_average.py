from average import Average

class SimpleMovingAverage(Average):
    
    def add_successive_points(self, point):
        self.average -= (self.points.popleft()) / self.set_size
        self.average += point / self.set_size

        self.points.append(point)

        return self.average

    def add_initial_points(self, point):
        self.points.append(point)
        self.average = sum(self.points) / len(self.points)

        return self.average
