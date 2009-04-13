#!/bin/env python

from choiceyana import circles

# Centres of 
circle_defs = {
    'start': [320, 380],
    't1': [190, 310],
    't2': [255, 217],
    't3': [385, 217],
    't4': [450, 310]}
target_names = ['t%d' % n for n in range(1,5)]

circle_class = circles.TouchCircle
circle_class.default_radius = 30

choicey_circles = circles.CircleCollection(
    [circle_class(name, *vals) for name, vals in circle_defs.items()]
    )

