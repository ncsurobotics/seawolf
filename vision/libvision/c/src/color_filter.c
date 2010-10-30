/**
 * \file
 * Color filter
 */

#include "vision_lib.h"

#include <cv.h>
#include <highgui.h>

/**
 * \ingroup colortools
 * \{
 */
 
/**
 * \brief a simple hard color filter.
 * colorfilter() recieves an image in the IplImage format, as well as six integers (0 through 256) 
 * which provide a minimum and maximum threshold for the red blue and green color values.  The
 * function checks each pixel in the image, and blacks out any that fall outside any of the 
 * specified color ranges.  The modified image is then returned.  
 *
 * Here is an example of basic usage:
 * \code
 * int minr =10, maxr = 100;
 * int minb =120, maxb = 256;
 * int ming =0, maxg = 50;
 * FilteredImage = colorfilter(Image, minr, maxr, minb, maxb, ming, maxg);
 * \endcode
 *
 * \param img the IplImage to be filtered
 * \param rmin the minimum red value 
 * \param rmax the maximum red value
 * \param gmin the minimum green value
 * \param gmax the maximum green value
 * \param bmin the minimum blue value
 * \param bmax the maximum blue value
 * \return an IplImage of the blacked-out origional image
 *
 */

IplImage* colorfilter(IplImage* img, int rmin, int rmax, int bmin, int bmax, int gmin, int gmax) {

  int y,x; 

  IplImage* color = cvCreateImage(cvGetSize(img),8,3);

  for(y=0; y<img->height; y++ ) {
    uchar* ptr = (uchar*) (img->imageData + y * img->widthStep);
    uchar* ptrN = (uchar*) (color->imageData + y * img->widthStep);

    for(x=0; x<img->width; x++ ) {
      
      //if not in range, black it out 
      if (!((ptr[3*x+2]>=rmin && ptr[3*x+2]<=rmax) &&
            (ptr[3*x+1]>=bmin && ptr[3*x+1]<=bmax) &&
            (ptr[3*x+0]>=gmin && ptr[3*x+0]<=gmax))) {
          ptrN[3*x+0] = ptrN[3*x+1] = ptrN[3*x+2] = 0;
      } else { // Copy value, don't adjust it
        ptrN[3*x+0] = ptr[3*x+0];
        ptrN[3*x+1] = ptr[3*x+1];
        ptrN[3*x+2] = ptr[3*x+2];
      } 
    }
  }

  return color; 
}
/** /} */
