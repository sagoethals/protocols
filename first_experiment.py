#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 17:44:38 2018

@author: sarah

First experiment: we switch between
- peak axonal current measurements
- threshold measurements
"""

from devices import *
from pylab import *
from protocols import *

nrec = 5

for rec in nrec:
    