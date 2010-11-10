==============
Vision Library
==============

The vision library is a collection of tools used for vision
processing. It contains computationally intensive algorithms written
in C and other useful algorithms written in Python. Because the
Vision Library does not contain any mission specific code, only
general algorithms, it is used from year to year. New functions will
be added as they are needed.

---------
Structure
---------

C code
``````
All C code is kept in the c/ folder.  The swig interface,
"interface.i" is also kept in that folder.  The C source is kept in
the c/src/ directory and the include files are in c/include/.

Python code
```````````
TODO

------------
Dependencies
------------
 * OpenCV
 * OpenCV Python SWIG interface.
    * If compiling OpenCV 2.0 from source, give cmake the
      -DBUILD_NEW_PYTHON_SUPPORT=ON option.
 * Swig
 * GCC
 * SCons

All can be installed easily through your linux distribution's
package manager.

---------
Compiling
---------
You only need to compile the C portion of the library.  To do this,
change directory into the c/ folder and run scons:

 $ cd c
 $ scons

This will build the swig interface and compile it.

-----
Using
-----
You will need to have the OpenCV SWIG Python interface in your
PYTHONPATH, as well as the software/vision/ directory (the directory
containing libvision).  You can then import the libvision package in python and use the library.

For detailed and well documented examples, look in the examples/
directory.

TODO: More on this
