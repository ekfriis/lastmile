==========================
Last Mile Designs Software
==========================

Software to support time definite delivery routing.

Packages
========

ants
----

An (incomplete) implementation of Ant Colony Optimization for solving
the assymetric traveling salesman problem with (specialized) time delivery
windows.

* http://en.wikipedia.org/wiki/Ant_colony_optimization
* http://en.wikipedia.org/wiki/Travelling_salesman_problem

Software requirements
=====================

* Python 2.4+

* Numpy (scipy.org)
* Google Maps api python interface (http://pypi.python.org/pypi/googlemaps/1.0.2)

On Mac/Linux (Windows?) you can install the dependencies by opening a terminal and typing:

   $ sudo easy_install numpy

   $ sudo easy_install googlemaps


Running the unit tests
----------------------

   $ cd lastmile

   $ python run_all_tests.py
