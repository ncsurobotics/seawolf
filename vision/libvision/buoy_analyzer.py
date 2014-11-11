
import ctypes
from . import cmodules


def buoy_analyzer(src, buoys):
    """Determine color of buoys in a single frame """

    if not len(buoys):
        return

    rois = (cmodules.BuoyROIStruct_p * len(buoys))()
    # extract regions of interest for each buoy
    for i, buoy in enumerate(buoys):
        buoy_struct = cmodules.BuoyROIStruct(buoy.x, buoy.y, buoy.width, buoy.width)
        rois[i] = ctypes.pointer(buoy_struct)

    color_sequence = cmodules.buoy_analyzer.buoy_color(src, rois, len(buoys))

    for i, buoy in enumerate(buoys):
        buoy.color = color_sequence[i]
