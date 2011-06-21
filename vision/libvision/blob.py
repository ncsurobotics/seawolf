
import ctypes
from . import cmodules

class Blob(object):
    def __init__(self, cblob):
        self.id = cblob.contents.id
        self.size = cblob.contents.size
        self.centroid = (cblob.contents.c_x, cblob.contents.c_y)

        # Region of interest - (x, y, width, height)
        self.roi = (cblob.contents.x_0, cblob.contents.y_0,
                    cblob.contents.x_1 - cblob.contents.x_0,
                    cblob.contents.y_1 - cblob.contents.y_0)

def find_blobs(img_in, img_out, min_blob_size, max_blobs):
    num_blobs = ctypes.c_int()
    cblobs = cmodules.cblob_mod._wrap_find_blobs(ctypes.py_object(img_in), ctypes.py_object(img_out), ctypes.pointer(num_blobs), min_blob_size, max_blobs)

    blobs = [Blob(cblobs[i]) for i in range(0, num_blobs.value)]
    cmodules.cblob_mod.free_blobs(cblobs, num_blobs)

    return blobs
