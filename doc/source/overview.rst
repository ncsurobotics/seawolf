
.. _overview:

Overview
===================================

Application Model
-----------------

Seawolf's software is organized into many independent applications.  Each
application runs in a separate process.  They can be run independently, making
for a highly modular design.  These applications communicate through a custom
made interprocess communication (IPC) library called `libseawolf
<http://opensource.ncsurobotics.com/docs/libseawolf/>`_.  libseawolf provides
shared variables and notifications between applications.  Each application
talks directly with a central server called the hub, as shown in this diagram:

.. graph:: hubgraph

   node [shape=Mrecord, style="filled", fillcolor="#aaddff", fontname="Sans"];
   edge [dir=both, arrowsize=0.9, color="#101020"];
   fontname="Sans";
   nodesep = 0.6;

   application_1:lib:s -- hub;
   application_2:lib:s -- hub;
   application_3:lib:s -- hub;

   subgraph cluster_applications {
     application_1 [label="{...|<lib> libseawolf}"];
     application_2 [label="{Application 2|<lib> libseawolf}"];
     application_3 [label="{Application 1|<lib> libseawolf}"];
     style = "filled, rounded";
     color = "#eeeeee";
   }
   hub [label="{Hub server|{libseawolf | db}}", fillcolor="#aaaaff"];

In Seawolf the term "Application" means a software component that uses the
libseawolf hub to communicate with other applications.  Although most
components in Seawolf use libseawolf, some do not.  Most notably SVR and vision
do not use libseawolf.

libseawolf is an open source project.  The `source code
<https://github.com/ncsurobotics/libseawolf>`_ and `documentation
<http://opensource.ncsurobotics.com/docs/libseawolf/>`_ are available online.

Software Components
-------------------

This diagram shows information flow for Seawolf's main components:

.. digraph:: components

    compound = true;
    node [shape=Mrecord, style="filled", height=0.3, fillcolor="#aaddff", fontname="Sans"];
    edge [arrowsize=0.9, color="#101020"];
    fontname = "Sans";
    ranksep = 0.7;

    subgraph cluster_software {
        label = "Software";
        compound = true;

        vision [label="Vision", fillcolor="#aaffdd", href="vision/index.html"];
        missioncontrol [label="Mission Control", href="mission_control/index.html"];
        svr [label="SVR", fillcolor="#aaffdd"];
        serialapp [label="Serial App", href="applications.html#serial-app"];
        mixer [label="Mixer", href="applications.html#mixer"];
        subgraph cluster_pid {
            compound=true;
            label = "PID Controllers";
            rank = same;
            depthpid [label="Depth", href="applications.html#pid-controllers"];
            yawpid [label="Yaw", href="applications.html#pid-controllers"];
            pitchpid [label="Pitch", href="applications.html#pid-controllers"];
        }

        svr -> vision;
        vision -> missioncontrol;
        missioncontrol -> yawpid [lhead=cluster_pid, len=0.5];
        yawpid -> mixer [ltail=cluster_pid];
        mixer -> serialapp;
        serialapp -> yawpid [lhead=cluster_pid];
    }

    subgraph cluster_hardware {
        rank = same;
        label = "Hardware";
        style = filled;
        color = lightgrey;

        microcontroller [label="Electronics", fillcolor="#ffddaa"];
        sensors [label="Sensors", fillcolor="#ffddaa"];
        cameras [label="Cameras", fillcolor="#ffddaa"];

        // Invisible nodes to make things look decent
        invis1 [style=invis];
        invis2 [style=invis];
        invis3 [style=invis];
        cameras -> invis1 -> invis2 -> invis3 -> sensors -> microcontroller [style=invis];
    }

    cameras -> svr;
    serialapp -> microcontroller;
    sensors -> serialapp;

The :ref:`Serial App <app_serial>` and :ref:`SVR <svr>` are the only software
components that communicate with the physical world.  The serial app handles
both input and output for microcontrollers, sensors and other peripherals.  SVR
captures frames from cameras and distributes them to any component that
requests a camera's input.

The :ref:`vision` component interprets images to give useful output to mission
control.  This is where almost all of Seawolf's processing time is spent.
Vision is usually run implicitly by mission control, although it can be run
separately for debugging purposes.

:ref:`mission_control` makes all navigational decisions.  It uses input from
vision as well as sensors.  Mission Control sets the PID setpoints to
accomplish this.

Together the :ref:`PID Controllers <app_pid>` and the :ref:`app_mixer` are used to control
the robot's movement.  The PIDs are given a desired sensor value (called the
setpoint) and they output thruster values that will move the robot accordingly.
The mixer then considers all of the thruster requests from the PIDs and mixes
them to produce the final thruster values (each from -1 to 1).

There are also many minor applications that are used on a daily basis while
running the software.  All applications are described in full in the
:ref:`applications` section.
