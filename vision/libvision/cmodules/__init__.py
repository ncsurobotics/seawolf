
'''
This package provides a way to call functions written in C, in a similar manner
to ctypes, but it handles conversion of IplImage types (and maybe more types in
the future) in arguments and return values.  This package is in fact a wrapper
around ctypes.


Using the Library
-----------------
The CModule class provides most of the intelligence behind this package.  After creating a CModule object, you can call it with the functions provided in the shared object file given.  For example:

>>> import cv
>>> from cmodule import CFunction, IplImage_p, CModule
>>>
>>> # Module Setup
>>> functions = [
>>>     CFunction("test_function", IplImage_p, [IplImage_p]),
>>> ]
>>> module = CModule("test.so", functions)
>>>
>>> # Calling a function
>>> image = cv.CreateImage((640,480), 8, 3)
>>> new_image = module.test_function(image)
>>>
>>> # Now both image and new_image are cv.iplimage types:
>>> type(image)
<type 'cv.iplimage'>
>>> type(new_image)
<type 'cv.iplimage'>

When using this package, you won't need to perform the module setup step at
all.  That step is already done in this file, you simply need to use the
CModule objects already instantiated in this file.  For example:
>>> import cv
>>> import cmodules
>>> image = cv.CreateImage((640,480), 8, 3)
>>> cmodules.test_function(image)


Creating a Module
------------------
To create a shared object file, simply create a .c file file in the src/
directory.  After running make, a corresponding .so file will be created.  You
can then specify the name of the .so file when instantiating a CModule object.

No C header file is needed.  Instead, define your functions and module by
instantiating a CModule object in this file.

Keep in mind, there are some limitations of the C functions.  It's a good idea
to know something about the conversion to and from IplImage_p before writing a
module.  At least read the section below about limitations before writing your own
module.


Limitations
-----------
TODO

'''
#TODO: Write Limitations section
#TODO: Where does documentation for modules go?

import ctypes

from cmodule import CModule, CFunction
from cvtypes import IplImage, IplImage_p, CvPoint


# Target Color Module

target_color = CModule("target_color.so", [
    CFunction("find_target_color", IplImage_p, [IplImage_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double])
])

# Target Color HSV Module

target_color_hsv = CModule("target_color_hsv.so", [
    CFunction("find_target_color_hsv", IplImage_p, [IplImage_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double])
])

# Shape Detect Module

shape_detect = CModule("shape_detect.so", [
    CFunction("detect_letters", None, [IplImage_p])
])  

# Instantiate CModule objects below:

test = CModule("test.so", [
    CFunction("test_function", IplImage_p, [IplImage_p]),
])

# blob module
class BlobStruct(ctypes.Structure):
    _fields_ = [
        ("top", ctypes.c_int),
        ("left", ctypes.c_int),
        ("right", ctypes.c_int),
        ("bottom", ctypes.c_int),
        ("area", ctypes.c_long),
        ("cent_x", ctypes.c_double),
        ("cent_y", ctypes.c_double),
        ("mid", CvPoint),
        ("pixels", ctypes.POINTER(CvPoint)),
    ]
BlobStruct_p = ctypes.POINTER(BlobStruct)
BlobStruct_p_p = ctypes.POINTER(BlobStruct_p)
blob = CModule("blob.so", [
    CFunction("find_blobs", ctypes.c_int, [IplImage_p, BlobStruct_p_p, ctypes.c_int, ctypes.c_int]),
    CFunction("blob_free", None, [BlobStruct_p, ctypes.c_int]),
])
