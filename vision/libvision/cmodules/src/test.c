
#include <highgui.h>

IplImage* test_function(IplImage* image) {
    IplImage* image_clone = cvCloneImage(image);
    cvCircle(image_clone, cvPoint(200, 200), 50, cvScalar(255,0,0,0), 1, 8, 0);
    return image_clone;
}
