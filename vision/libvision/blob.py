
import ctypes
from . import cmodules


class Blob(object):

    def __init__(self, cblob):
        # Id of blob. This is the index used in the image output by find_blobs
        # for this blob
        self.id = cblob.contents.id

        # Pixels contained by the blob
        self.size = cblob.contents.size

        # Center of mass, 'centroid'. This is a CvPoint
        self.centroid = (cblob.contents.c_x, cblob.contents.c_y)

        # Region of interest. This is a RvRect
        self.roi = (cblob.contents.x_0, cblob.contents.y_0,
                    cblob.contents.x_1 - cblob.contents.x_0,
                    cblob.contents.y_1 - cblob.contents.y_0)


def find_blobs(img_in, img_out, min_blob_size, max_blobs, out_coloring=0):
    """ find_blobs(img_in, img_out, min_blob_size, max_blobs, out_coloring=0)

    Locate blobs in the binary image img_in. Choose blobs having at least
    min_blob_size pixels, and choose no more than max_blobs. The blobs which
    mean these requirements are returned as a list, and also written to the
    indexed image img_out. The index of a pixel in img_out is the id of the blob
    it belongs too (with 0 being no blob).

    """

    num_blobs = ctypes.c_int()
    cblobs = cmodules.cblob_mod._wrap_find_blobs(ctypes.py_object(img_in), ctypes.py_object(img_out), ctypes.pointer(num_blobs), min_blob_size, max_blobs, out_coloring)

    blobs = [Blob(cblobs[i]) for i in range(0, num_blobs.value)]
    cmodules.cblob_mod.free_blobs(cblobs, num_blobs)

    return blobs
