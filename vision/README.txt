The Seawolf vision system is responsible for finding objects, or entities,
through cameras and reporting their location and orientation relative to
Seawolf.  This information is reported back to mission control, which uses the
information to move the robot and complete missions.

An entity is a vision object, something that is part of the competition that we
want to be able to see.  We call them entities, and not objects because the
word "object" can conflict with a few different meanings, and "entity" is much
clearer and concise.

===============
Getting Started
===============

Dependencies
------------

- Python 2.6 or higher (but earlier than 3.0)
- OpenCV 2.2 (2.0 or later might work, but 2.2 is strongly recommended)
- OpenCV Python bindings (should be installed by default)
    You will have to add the directory that these are installed in (probably
    /usr/local/lib/python2.X/site-packages/) to your PYTHONPATH.

Using run.py
------------
run.py is a script that runs vision, much like mission control would, but it
simply prints out any objects that are found instead of moving the robot
accordingly.  run.py is useful for testing and debugging vision code.

One of the entities that can be searched for is an example entitiy, called
"example".  We will use it in our first execution of run.py:

    $ python run.py -c down 0 example

The -c option specifies the camera "down" to use the index 0.  The example
entity uses the "down" camera.  The name "example" is given as an argument to
specify that the example entity should be searched for.  For a list of entities
that can be searched for, use the -h, or --help option.  This will also give
you a list of cameras which entities use.

For more information and options for run.py execute the script with the --help
option.

==========
Developing
==========

Entities
--------
The code for all entities is stored under the entities/ directory in
corresponding files.  For documentation on how entities are written, see the
entity base class in "entities/base.py".  The example entitiy is meant to be a
basic tutorial on the subject.

Note that when adding an entity, you will have to modify entities/__init__.py

Multiprocessing Internals
-------------------------
The vision system uses a multiprocessing architecture.  This can be useful to
know when developing and debugging.

TODO: More detail
