
.. _overview:

Overview
===================================

Application Model
-----------------

Seawolf's software is organized into different applications.  Each application
runs in a separate process.  They can be run independently, making for a highly
modular design.  These applications communicate through a custom made
interprocess communication (IPC) library called `libseawolf
<http://opensource.ncsurobotics.com/docs/libseawolf/>`_.  libseawolf provides
shared variables and notifications between applications.  Each application
talks directly with a central server called the hub:

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

libseawolf is an open source project.  The `source code
<https://github.com/ncsurobotics/libseawolf>`_ and `documentation
<http://opensource.ncsurobotics.com/docs/libseawolf/>`_ are available online.

Application Structure
---------------------

Although applications never communicate to eachother directly, it is useful to
think of how information flows between them.  This diagram shows information
flow for seawolf's main applications:

.. digraph:: completeapp

   node [shape=Mrecord, style="filled", height=0.3, fillcolor="#aaddff", fontname="Sans"];
   edge [arrowsize=0.9, color="#101020"];
   fontname="Sans";

   subgraph cluster_applications {
     label = "Applications";

     svr [label="SVR"];
     vision [label="Vision"];
     missioncontrol [label="Mission Control"];
     mixer [label="Mixer", href="applications/mixer.html"];
     serialapp [label="Serial App"];

     depthpid [label="Depth PID"];
     yawpid [label="Yaw PID"];

     svr -> vision;
     vision -> missioncontrol;
     missioncontrol -> depthpid;
     missioncontrol -> yawpid;
     depthpid -> mixer;
     yawpid -> mixer;
     mixer -> serialapp;
     serialapp -> missioncontrol;
   }

   cameras -> svr;
   imu -> serialapp;
   serialapp -> thrusters;

   subgraph cluster_environment {
     style = filled;
     color = lightgrey;

     // Invisible arrows to arrange the bubbles nicely.
     edge [style=invisible, arrowtype=none, arrowsize=0];
     cameras -> thrusters -> imu;

     cameras [label="Cameras", fillcolor="#ffddaa"];

     // Show thrusters and IMU on same row
     subgraph {
       rank = same;

       imu [label="IMU", fillcolor="#ffddaa"];
       thrusters [label="Thrusters", fillcolor="#ffddaa"];
     }

     label = "Environment";
   }

.. todo:: Application structure
