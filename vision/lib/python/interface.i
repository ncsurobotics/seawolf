
%module libvision

%{
#include <cv.h>
#include <highgui.h>

#include "vision_lib.h"
%}

%typemap(in) IplImage* {
    CvMat* mat_p = NULL;
    if ((SWIG_ConvertPtr($input, (void**) &mat_p, $descriptor(CvMat*), SWIG_POINTER_EXCEPTION)) == -1) return NULL;
    $1 = (IplImage*) cvAlloc(sizeof(IplImage));
    $1 = cvGetImage(mat_p, $1);
}

/* Prototypes that are commented out are in the .h file, but not the
 * corresponding .c file!
 */

/* normalize.h */ 
IplImage* normalize_image(IplImage* img);

/* blob.h */
int blob(IplImage* Img, BLOB** blobs, int tracking_number, int minimum_blob_area);
BLOB* findPrimary(IplImage* Img, int target_number, int minimum_blob_area, int *blobs_found);
int checkPixel(IplImage* Img, int x, int y, unsigned int** pixlog, BLOB* blob, int depth); 
void blob_copy(BLOB* dest, BLOB* src);
void blob_free(BLOB* blobs, int blobs_found);

/* color_filter.h */
IplImage* colorfilter(IplImage* img, int rmin, int rmax, int bmin, int bmax, int gmin, int gmax);

/* edge.h */
IplImage* edge_opencv(IplImage* frame, int low_threshold, int high_threshold, int aperture);

/* hough.h */
/* void hough_init(void); */
/* void houghMouseDraw(int event, int x, int y, int flags, void* param); */
CvSeq* hough(IplImage* img, IplImage* original, int threshold, int linesMax,int targetAngle, int angleThreshold, int clusterSize, int clusterWidth, int clusterHeight);
void hough_draw_lines(IplImage* image, CvSeq* lines);

/* remove_edges.h */
/* void remove_edges_init(void); */
IplImage* remove_edges(IplImage* img, IplImage* edge, int rmin, int rmax, int bmin, int bmax, int gmin, int gmax);
/* void remove_edges_free(void); */

/* target_color.h */
int FindTargetColor(IplImage* in, IplImage* out, RGBPixel* color, int min_blobsize, int dev_threshold, double precision_threshold);
float Pixel_stddev(RGBPixel* px_1, RGBPixel* px_2);
