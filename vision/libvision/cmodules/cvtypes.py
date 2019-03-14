
'''Contains structures that mimick types from OpenCV.'''

import ctypes
c_char_p = ctypes.POINTER(ctypes.c_char)


class IplImage(ctypes.Structure):

    '''A copy of OpenCV's IplImage structure.

    You can specify this as an argument type or return type in a CFunction
    object.  The CModule object will handle the conversion to and from the
    Python IplImage type that OpenCV provides as part of its new Python
    interface.
    '''
    _fields_ = [
        ("nSize", ctypes.c_int),
        ("ID", ctypes.c_int),
        ("nChannels", ctypes.c_int),
        ("alphaChannel", ctypes.c_int),
        ("depth", ctypes.c_int),
        ("colorModel", ctypes.c_char * 4),
        ("channelSeq", ctypes.c_char * 4),
        ("dataOrder", ctypes.c_int),
        ("origin", ctypes.c_int),
        ("align", ctypes.c_int),
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("roi", ctypes.c_void_p),
        ("maskROI", ctypes.c_void_p),
        ("imageId", ctypes.c_void_p),
        ("tileInfo", ctypes.c_void_p),
        ("imageSize", ctypes.c_int),
        ("imageData", c_char_p),
        ("widthStep", ctypes.c_int),
        ("BorderMode", ctypes.c_int * 4),
        ("BorderConst", ctypes.c_int * 4),
        ("imageDataOrigin", c_char_p),
    ]
IplImage_p = ctypes.POINTER(IplImage)


class CvPoint(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_int),
        ("y", ctypes.c_int),
    ]
