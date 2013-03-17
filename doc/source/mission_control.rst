
.. _mission_control:

Mission Control
===================================

Mission control makes navigational decisions based mostly on information from
:ref:`vision`.  As missions get completed, mission control goes through a list
of missions sequentially.

Mission control starts an instance of the vision component implicitly when it
starts.  This is because the communication between the two go through a Python
multiprocessing pipe, allowing for Python objects to be sent between them.

Running
-------

To run mission control, go into the ``mission_control/`` directory and execute ``run.py``:

    $ cd mission_control/
    $ python run.py

This will start on the first mission, using svr streams for each camera used.

Only some options were described here.  To get a descriptions of all options,
run mission control with the -h option::

    $ python run.py -h

--wait-for-go
-w

--initial-mission <index>
-i <index>

--camrea <camera> <index>
-c <camera> <index>

--non-graphical
-G

.. todo:  Specifying Cameras

Writing Missions
----------------

.. todo:: Document Missions

sw3 Library
-----------

.. todo:: Document sw3 lib
