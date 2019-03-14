
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
# TODO: Write Limitations section
# TODO: Where does documentation for modules go?

import ctypes

from cmodule import CModule, CFunction
from cvtypes import IplImage, IplImage_p, CvPoint


# Target Color Module

target_color_rgb = CModule("target_color_rgb.so", [
    CFunction("find_target_color_rgb", IplImage_p, [IplImage_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double])
])

# Target Color HSV Module

target_color_hsv = CModule("target_color_hsv.so", [
    CFunction("find_target_color_hsv", IplImage_p, [IplImage_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double])
])

# Shape Detect Module


class cRect(ctypes.Structure):
    _fields_ = [
        ("area", ctypes.c_int32),
        ("c_x", ctypes.c_int32),
        ("c_y", ctypes.c_int32),
        ("theta", ctypes.c_int32),
    ]

cRect_p = ctypes.POINTER(cRect)
cRect_p_p = ctypes.POINTER(cRect_p)

shape_detect = CModule("shape_detect.so", [
    CFunction("match_letters", ctypes.c_int, [IplImage_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]),
    CFunction("find_bins", cRect_p_p, [IplImage_p, ctypes.POINTER(ctypes.c_int)]),
    CFunction("free_bins", None, [cRect_p_p, ctypes.c_int])
])

# Buoy Analysis Module


class BuoyROIStruct(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_int),
        ("y", ctypes.c_int),
        ("w", ctypes.c_int),
        ("h", ctypes.c_int),
    ]
BuoyROIStruct_p = ctypes.POINTER(BuoyROIStruct)
BuoyROIStruct_p_p = ctypes.POINTER(BuoyROIStruct_p)
buoy_analyzer = CModule("buoy_analyzer.so", [
    CFunction("buoy_color", ctypes.POINTER(ctypes.c_int), [IplImage_p, BuoyROIStruct_p_p, ctypes.c_int])
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


class cBlob(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_uint32),
        ("size", ctypes.c_int32),
        ("c_x", ctypes.c_uint32),
        ("c_y", ctypes.c_uint32),
        ("x_0", ctypes.c_uint16),
        ("x_1", ctypes.c_uint16),
        ("y_0", ctypes.c_uint16),
        ("y_1", ctypes.c_uint16)
    ]

cBlob_p = ctypes.POINTER(cBlob)
cBlob_p_p = ctypes.POINTER(cBlob_p)

cblob_mod = CModule("blob2.so", [
    CFunction("_wrap_find_blobs", cBlob_p_p, [ctypes.py_object, ctypes.py_object, ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int, ctypes.c_int]),
    CFunction("free_blobs", None, [cBlob_p_p, ctypes.c_int])
])

cgreymap_mod = CModule("greymap.so", [
    CFunction("_wrap_greymap", None, [ctypes.py_object, ctypes.py_object, ctypes.c_ubyte * 256])
])
