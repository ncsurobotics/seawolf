
.. _applications:

Applications
===================================

The software is broken into many applications which run as their own process.
This is the basis of Seawolf's highly modular software design.  These
applications communicate using libseawolf shared variables and notifications.

Most notable applications are documented here.  Some small applications are not
described in detail.  Larger applications such as :ref:`mission control
<mission_control>` and the :ref:`simulator <sim>` have their own section.

.. contents::
   :backlinks: none

Running Applications
--------------------

Most applications are located in the `applications/` folder.  Larger
applications, such as the :ref:`app_serial` are located in their own toplevel
folder.  When running applications, you must be in a specific folder, or the
application won't be able to find ``seawolf.conf``, since the file is specified
relative to the current directory.

Inside ``applications/`` there is ``src/`` and ``bin/``.  Run ``make`` inside ``applications/`` and it will compile each application source file inside ``src/`` to a binary executable in ``bin/``.  To run these applications, navigate to the ``applications/`` directory and run ``./bin/<application>``.  For example:

.. code-block:: bash

    seawolf5$ cd applications/
    seawolf5/applications$ ./bin/mixer
    [PID Mixer][INFO] Initialized
    [PID Mixer][DEBUG] 0.00 updates/sec
    ...

The serial app other larger applications are run similarly.

.. _app_runner:

Application Runner
``````````````````

The application runner allows for easily running Seawolf applications through a
GUI interface.  Although it is much less flexible than the command line, it can
be a lot easier to use.

.. todo:: Application Runner
    Include description and usage here.  run.rst will link to here.

.. automodule:: run
.. .. autocommand:: python run.py -h
..    :show_command:


Application Descriptions
------------------------

.. _app_pid:

PID Controllers
```````````````

Each PID controller is used to get the robot from one state to another
smoothly.  For example, the yaw PID tries to point the robot in a given
direction.  PIDs try not to overshoot or undershoot their goal.

PIDs determine their output (thruster values) by the addition of three
different terms: proportional, integral and differential (hence the name PID).
The weight of these three terms are set by corresponding constant values: the
``p``, ``i``, and ``d`` constants.  Since these are used to tune the behavior
of the PID controller, they are also called tuning constants.  The details of
how a PID controller works will not be covered here, but there are numerous
online resources on the subject.

The main PIDs in Seawolf are Depth and Yaw.  Seawolf is stable enough that Roll
and Pitch correction is usually not needed.  All PIDs are in the ``applications/``
directory, named depthpid, yawpid, etc.

**Input:**

libseawolf variables:
 * ``<pid name>PID.Paused`` - If ``1``, pause.  If ``0``, run.
 * ``<pid name>PID.Heading`` - The setpoint, used to calculate the error.
 * ``<pid name>PID.p`` - Proportional constant.
 * ``<pid name>PID.i`` - Integral constant.
 * ``<pid name>PID.d`` - Differential constant.

**Output:**

libseawolf Notification with action ``THRUSTER_REQUEST`` and param ``<pid name>
value1 [value2 ...]``.  The number of values sent and what they mean depend on
the PID.

.. _app_mixer:

Mixer
`````

Recieves requests from PIDs and mixes them together, producing final thruster
values from -1 to 1.

A thruster request with value 1 or -1 does not guarentee that any
thrusters will be set to maximum.  This is because the mixing algorithm is not
nessesarily as simple as adding requests from each PID together.

**Input:**

Notifications with action ``THRUSTER_REQUEST`` sent by PID controllers.  See :ref:`app_pid` for details.

**Output:**

Sets libseawolf variables for thrusters to values from -1 to 1.

.. _app_serial:

Serial App
``````````

.. todo:: Document Serial App


Writing Applications
--------------------

.. todo:: Writing applications

Adding to the Application Runner
````````````````````````````````

.. todo:: Adding to app runner
