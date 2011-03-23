
from time import time
from os import path

import cv
import ctypes

libvision_dc1394_directory = path.abspath(__file__)
dc1394_so_file = path.realpath(
    path.join(libvision_dc1394_directory, "../dc1394.so")
)
try:
    dc = ctypes.cdll.LoadLibrary(dc1394_so_file)
except OSError:
    raise OSError('Could not find "dc1394.so". Did you forget to compile libvision?')
dc.grab_frame.restype = ctypes.POINTER( ctypes.c_char )

class DC1394Camera(object):
    '''Represents a firewire camera through the dc1394 library.'''

    def __init__(self, index):
        self.index = index
        self.dc_camera = dc.open_camera(index)
        if not self.dc_camera:
            raise IOError("Problem opening firewire camera! (See error printed above)");

        self.width = dc.get_width(self.dc_camera)
        self.height = dc.get_height(self.dc_camera)
        self.num_channels = dc.get_channels(self.dc_camera)

    def get_frame(self):
        image_data = dc.grab_frame(self.dc_camera)

        if not image_data:
            raise IOError("Problem getting frame from firewire camera! (See error printed above)");

        frame = cv.CreateImageHeader((self.width, self.height), 8, self.num_channels)
        cv.SetData(frame, image_data[:self.width*self.height*self.num_channels])

        cv.ConvertImage(frame, frame, cv.CV_CVTIMG_SWAP_RB)
        dc.free_image_data(image_data)
        return frame

    def close(self):
        if dc and self.dc_camera:
            dc.close_camera(self.dc_camera)
    __del__ = close
