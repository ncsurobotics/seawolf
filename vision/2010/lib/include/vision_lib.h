/* \file
 * Main include file.
 */

/**
 * \mainpage
 * The seawolf vision library includes many vision processing tools.  The
 * library is made to be fast and easy to use.
 *
 */

/**
 * \defgroup blob Blob Tools
 * \brief provides blob-finding tools.
 * Provides a BLOB data structure and tools for detecting blobs.  Most prominantly,
 * it contains the function blob() that finds and returns blobs of non-black pixels in
 * an image
 */
 
/**
* \defgroup colortools Color Tools
* \brief Contains color-based image processing tools.
* The two color-based tools current written are: 
* - colorfilter() , a simple hard color filter
* - FindTargetColor(), a smarter color-matching tool, generaly more useful than a hard color filter
*/

/** 
* \defgroup edgetools Edge Tools
* \brief Containes tools for detecting and modifying edges of an image. 
* The current tools in this module are:
* - edge_opencv() calls open cv's sobel edge detect function
* - remove_edges() a specialized function written to help detect vertical poles underwater
* - hough() a modification of open cv's hough transform, used to detect straight lines
*/

#ifndef __SEAWOLF_VISION_LIB_ROOT_INCLUDE_H
#define __SEAWOLF_VISION_LIB_ROOT_INCLUDE_H

#include <cv.h>
#include <highgui.h>
#include <stdbool.h>

/* All Seawolf Vision Lib headers */
#include "vision_lib/blob.h"
#include "vision_lib/camera.h"
#include "vision_lib/color_filter.h"
#include "vision_lib/hough.h"
#include "vision_lib/edge.h"
#include "vision_lib/normalize.h"
#include "vision_lib/remove_edges.h"
#include "vision_lib/target_color.h"

#endif // __SEAWOLF_VISION_LIB_ROOT_INCLUDE_H
