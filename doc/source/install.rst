
.. _install:

Installing
===================================

Requirements
------------

Only Linux is supported.  Debian and Ubuntu are the most tested distributions.
Package names given here are Debian and Ubuntu packages, although other
distributions likely have very similar or identical package names.  For the
bare minimum, you need:

* Essential development tools (GCC, make...) (package ``build-essential``)
* Python 2.6 or 2.7 (package ``python2.x``, replace x with 6 or 7)
* Git (package ``git``)

.. todo:: Link to OpenCV install tutorial here.

To run :ref:`vision` you will also need OpenCV >= 2.2 (with Python bindings).
This may need to be installed from source to get a late enough version.  For
more information visit their `website <http://opencv.willowgarage.com/wiki/>`_

To run the :ref:`sim`, in addition to OpenCV, you will also need OpenGL Python
Bindings (package ``python-opengl``).

On Debian or Ubuntu, you would use the ``apt-get`` command to install these packages.  For example::

    $ sudo apt-get install python2.6

Custom Libraries
----------------

First, open up a command prompt and create a directory for software and go into
that directory::

   $ mkdir software
   $ cd software

Inside this directory we will put the required software repositories.  You can
find all of Seawolf's repositories on Github under the `ncsurobotics
organization <https://github.com/ncsurobotics>`_.  To download one of the
repositories, go to the repository's main page and find its URL.  There is more
than one URL for each repo that you can use, the details of which I won't go
into.  Github has some nice `help pages <http://help.github.com/>`_ you can
reference if you have trouble, or just want to learn more.

Use the ``git clone`` command to get a local copy of the repo onto your
computer::

    $ git clone <url>

For example, to get a copy of libseawolf, run this command::

    $ git clone git@github.com:ncsurobotics/libseawolf.git

This will create a directory called libseawolf inside your current directory.
These repos have a ``README`` file that describes how to compile and install.
Go ahead and download the following repos and install them:

* libseawolf
* swpycv - Dependancy for vision and svr.
* svr - Only required for running vision or simulator.

Main Repository
---------------

The main software repository is named ``seawolf5``.  Download this into your
software folder just like the other repositories.

.. todo:: Write this section...
