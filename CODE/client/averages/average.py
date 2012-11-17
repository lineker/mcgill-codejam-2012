"""
Interface for all Average classes.

Provides a standard way to access and update data for a particular algorithm. 
"""

from collections import deque
from json import dumps

class Average:
    """
    Attributes:
        average  -- the current average at a particular tick
        time     -- the current time tick for this average
        set_size -- the subset size for this moving average
        points   -- the list of points currently part of the moving average
    """

    def __init__(self, set_size):
        """
        Initializes a new Average instance with a particular subset size.

        Parameters:
            set_size -- the subset size for this moving average
        """

        self.average = 0
        self.time = 0
        self.price = None
        self.set_size = set_size
        self.points = deque([])

    def update(self, point):
        """
        Updates this Average instance with a new point.
        Handles both the situation where we have less than `set_size` points
        and also when we are adding successive values.

        Parameters:
            point   -- the next value obtained in our data set

        Returns:
            average -- the newly updated average after adding the point
        """

        if len(self.points) < self.set_size:
            self.average = self.add_initial_points(float(point))
        else:
            self.average = self.add_successive_points(float(point))

        self.time += 1
        self.price = float(point)

        return self.average

    def add_successive_points(self, point):
        """
        Abstract method.

        Adds a successive point when there are already `set_size` points in
        our list, and re-calculates the average.

        Parameters:
            point   -- the next value obtained in our data set

        Returns:
            average -- the newly updated average after adding the point
        """

        raise NotImplementedError("add_successive_points not yet implemented")

    def add_initial_points(self, point):
        """
        Abstract method.

        Adds a successive point when there are less than `set_size` points in
        our list, and re-calculates the average.

        Parameters:
            point   -- the next value obtained in our data set

        Returns:
            average -- the newly updated average after adding the point
        """
        raise NotImplementedError("add_initial_points not yet implemented")

    def to_json(self):
        """
        Serializes moving average data to JSON.
        """

        return dumps({
                "price": self.price, 
                "time": self.time, 
                "average": self.average})
