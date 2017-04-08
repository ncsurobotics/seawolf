
'''
Provides the CModule class, which is the main intelligence behind the
c_module package.
'''

from collections import namedtuple
from os import path
import ctypes

import cv

from cvtypes import IplImage, IplImage_p

SOURCE_DIRECTORY = path.realpath(
    path.join(path.abspath(__file__), "../src/")
)

CFunction = namedtuple("CFunction",
                       ['name', 'return_type', 'argument_types']
                       )


def iplimage_errcheck(iplimage_pointer, func, arguments):
    '''Convert an IplImage struct into an OpenCV Python object.

    This function should be used only for IplImages that were created in C code
    and returned as a return value from a C function.
    '''
    # TODO: It seems that widthStep doesn't get set correctly here.  The
    #      structure has the correct widthStep, but I don't know how to set
    #      widthStep on the Python IplImage type.

    iplimage = iplimage_pointer.contents
    converted_image = cv.CreateImageHeader((iplimage.width, iplimage.height),
                                           iplimage.depth, iplimage.nChannels)
    cv.SetData(converted_image,
               iplimage.imageData[:iplimage.width * iplimage.height * iplimage.nChannels])
    _internal_c.releaseImage(iplimage_pointer)
    return converted_image


def to_iplimage_p(image):
    '''Turns an OpenCV Python IplImage type into a ctypes struct.'''
    image_data = ctypes.create_string_buffer(image.tostring())
    Four_C_Int = ctypes.c_int * 4
    Four_C_Char = ctypes.c_char * 4
    iplimage_struct = IplImage(
        nSize=ctypes.sizeof(IplImage),
        ID=0,  # Ignored by OpenCV
        nChannels=image.nChannels,
        alphaChannel=0,  # Ignored by OpenCV
        depth=image.depth,
        colorModel="0000",  # Ignored by OpenCV
        channelSeq="0000",  # Ignored by OpenCV
        dataOrder=0,  # Interleaved color channels
        origin=0,  # Top left
        align=4,  # Ignored by OpenCV
        width=image.width,
        height=image.height,
        roi=ctypes.c_void_p(),  # No ROI
        maskROI=ctypes.c_void_p(),  # Ignored by OpenCV
        imageId=ctypes.c_void_p(),  # Ignored by OpenCV
        tileInfo=ctypes.c_void_p(),  # Ignored by OpenCV
        imageSize=image.width * image.height * image.nChannels,
        imageData=image_data,
        widthStep=image.width * image.nChannels,
        BorderMode=Four_C_Int(0, 0, 0, 0),  # Ignored by OpenCV
        BorderConst=Four_C_Int(0, 0, 0, 0),  # Ignored by OpenCV
        imageDataOrigin=image_data,
    )
    return ctypes.pointer(iplimage_struct)


class CModule(object):

    '''Represents a shared object that can be called from Python.

    This class is a wrapper around ctypes that handles the conversion of
    OpenCV's IplImage type in arguments and return values.  The IplImage_p type
    may be given as either a return type or argument type.  In this case, a
    Python IplImage object as provided by the new Python interface of OpenCV
    will be expected or returned.

    After instantiating this class, you can call the methods in a similar
    manner to ctypes.  For example:
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

    Arguments:

        file_name - The filename of the .so file that will be used.  Since the
            MakeFile creates all shared objects in the src/ directory, all
            paths are relative to the src/ directory.  The MakeFile creates .so
            files for every .c file, with the same name except for the .so
            extension.

        functions - A list of CFunction objects.  Each CFunction represents a
            function that can be called in this object.

    '''
    # TODO: Check argument types for IplImage_p
    # TODO: Check number of arguments and return a reasonable error.

    def __init__(self, file_name, functions):
        self.file_name = file_name
        self.functions = {}
        for function in functions:
            self.functions[function.name] = function
        self.ctypes_object = None

    def open_shared_object(self):
        '''Open the ctypes object for the underlying shared object.'''

        object_file_name = path.join(SOURCE_DIRECTORY, self.file_name)
        try:
            self.ctypes_object = ctypes.cdll.LoadLibrary(object_file_name)
        except OSError as e:
            raise OSError('Could open "%s". Did you forget to compile libvision?  Error: %s' % (object_file_name, e))

        for name, return_type, argument_types in self.functions.itervalues():
            func = getattr(self.ctypes_object, name)

            func.restype = return_type
            func.argtypes = argument_types

            if return_type is ctypes.POINTER(IplImage):
                func.errcheck = iplimage_errcheck

    def __getattr__(self, function_name):
        '''
        Returns the function corresponding to function_name.  Raises an
        AttributeError when the function isn't found.
        '''

        if not self.ctypes_object:
            self.open_shared_object()

        try:
            name, return_type, argument_types = self.functions[function_name]
        except KeyError:
            raise AttributeError("Function not found in module.")

        func = getattr(self.ctypes_object, name)

        # If the function has no IplImage_p types, it doesn't need to be
        # wrapped.
        if IplImage_p not in argument_types:
            return func

        def func_wrapper(*args):
            '''
            Wraps the ctypes object so that all IplImage_p type arguments are
            converted correctly.
            '''
            arguments = []
            for i, arg_type in enumerate(argument_types):
                if arg_type is IplImage_p:
                    arguments.append(to_iplimage_p(args[i]))
                else:
                    arguments.append(args[i])
            return func(*tuple(arguments))

        return func_wrapper

# Used internally to free memory from a returned IplImage*
_internal_c = CModule("internal.so", [
    CFunction("releaseImage", None, [ctypes.c_void_p])])
