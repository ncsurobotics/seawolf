
import ctypes
from . import cmodules


def greymap(img_in, img_out, mapping):
    if len(mapping) != 256:
        raise Exception("Greyscale mapping must providing mapping of 256 bytes")

    array_type = ctypes.c_ubyte * 256
    cmodules.cgreymap_mod._wrap_greymap(ctypes.py_object(img_in),
                                        ctypes.py_object(img_out),
                                        array_type(*mapping))
