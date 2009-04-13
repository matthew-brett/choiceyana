#!/bin/env python
''' Detecting circles within coordinates '''

import numpy as np

class TouchCircle(object):
    default_radius = 30
    def __init__(self, name, X, Y, radius=None):
        if radius is None:
            radius = self.default_radius
        self.name = name
        self.XY = np.array([X, Y])
        self.radius = radius

    def distance(self, X1, Y1):
        if X1 is None or Y1 is None:
            return None
        XY1 = np.array([X1, Y1])
        return np.sqrt(np.sum((XY1-self.XY)**2))
    
    def inside(self, X1, Y1):
        dist = self.distance(X1, Y1)
        if dist is None:
            return None
        return dist <= self.radius


class CircleCollection(object):
    def __init__(self, circlelist):
        self.list = circlelist

    def inside_which(self, X1, Y1):
        for c in self.list:
            if c.inside(X1, Y1):
                return c

    def inside_which_name(self, X1, Y1):
        c = self.inside_which(X1, Y1)
        if c is None:
            return None
        return c.name
    
    def nearest(self, X1, Y1):
        dists = [c.distance(X1, Y1) for c in self_list]
