
#include <highgui.h>

void releaseImage(IplImage* image) {
    cvReleaseImage(&image);
}
