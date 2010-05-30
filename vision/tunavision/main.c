
#include "seawolf.h"
#include "img.h"

#include <opencv/cv.h>
#include <opencv/highgui.h>

#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    Image* img_src = NULL;
    Image* rgb_tmp = NULL;
    Image* indexed_tmp = NULL;
    RGBPixel color = {0xff, 0x40, 0x00};
    Timer* timer = Timer_new();
    int i = 0;

#ifdef TUNADEBUG
    IplImage* ipl_src = NULL;
    IplImage* ipl_out1 = NULL;
    IplImage* ipl_out2 = NULL;
    IplImage* ipl_out3 = NULL;
    IplImage* ipl_out4 = NULL;

    const char* src = "Controls";
    const char* out1 = "Normalized";
    const char* out2 = "Blur/Reduced";
    const char* out3 = "Color Filter";
    const char* out4 = "Blob";
    
    int w = 450;
    int h = 300;
    int s = 400;

    cvNamedWindow(src, 0);
    cvNamedWindow(out1, 0);
    cvNamedWindow(out2, 0);
    cvNamedWindow(out3, 0);
    cvNamedWindow(out4, 0);

    cvMoveWindow(src, 10, 10);
    cvMoveWindow(out1, s + 20, 10);
    cvMoveWindow(out2, s + w + 40, 10);
    cvMoveWindow(out3, s + 20, 10 + h + 50);
    cvMoveWindow(out4, s + w + 40, 10 + h + 50);

    cvResizeWindow(src, s, 500);
    cvResizeWindow(out1, w, h);
    cvResizeWindow(out2, w, h);
    cvResizeWindow(out3, w, h);
    cvResizeWindow(out4, w, h);
#endif
    
    int blur = 1,
        colorCount = 8,
        colorThreshold = 16,
        colorFilterCount = 1,
        nr = 10,
        normalize = 128,
        edge = 16;
        
#ifdef TUNADEBUG
    cvCreateTrackbar("Noise", src, &nr, 128, NULL);
    cvCreateTrackbar("Normalize", src, &normalize, 256, NULL);
    cvCreateTrackbar("Edge", src, &edge, 64, NULL);
    cvCreateTrackbar("Blur Rounds", src, &blur, 16, NULL);
    cvCreateTrackbar("Palette Count", src, &colorCount, 64, NULL);
    cvCreateTrackbar("Palette Sensitivity", src, &colorThreshold, 128, NULL);
    cvCreateTrackbar("Filter Choose", src, &colorFilterCount, 64, NULL);
#endif

    /* Initialize temporary images */
    img_src = Bitmap_read("in.bmp");

    rgb_tmp = Image_new(RGB, img_src->width, img_src->height);
    indexed_tmp = Image_new(INDEXED, img_src->width, img_src->height);

#ifdef TUNADEBUG
    ipl_src = cvCreateImage(cvSize(rgb_tmp->width, rgb_tmp->height), IPL_DEPTH_8U, 3);
    ipl_out1 = cvCreateImage(cvSize(rgb_tmp->width, rgb_tmp->height), IPL_DEPTH_8U, 3);
    ipl_out2 = cvCreateImage(cvSize(rgb_tmp->width, rgb_tmp->height), IPL_DEPTH_8U, 3);
    ipl_out3 = cvCreateImage(cvSize(rgb_tmp->width, rgb_tmp->height), IPL_DEPTH_8U, 3);
    ipl_out4 = cvCreateImage(cvSize(rgb_tmp->width, rgb_tmp->height), IPL_DEPTH_8U, 3);
#endif    

    Timer_reset(timer);
#ifdef TUNADEBUG
    while(cvWaitKey(50) != 'q') {
#else
    while(true) {
#endif
        Image_copy(img_src, rgb_tmp);

#ifdef TUNADEBUG
        ImageToIplImage(rgb_tmp, ipl_src);
        cvShowImage(src, ipl_src);
#endif

        if(normalize) {
            //Image_nr(rgb_tmp, rgb_tmp, nr);
            if(normalize > 16) {
                Image_normalize(rgb_tmp, rgb_tmp, normalize);
            }
            Image_edgeDetect(rgb_tmp, rgb_tmp, edge);
        } else {
            Image_toGrayscale(rgb_tmp, indexed_tmp);
            Image_indexedToRGB(indexed_tmp, rgb_tmp);
        }

#ifdef TUNADEBUG
        ImageToIplImage(rgb_tmp, ipl_out1);
        cvShowImage(out1, ipl_out1);
#endif
        
        Image_reduceSpectrum(rgb_tmp, indexed_tmp, colorCount, colorThreshold);

#ifdef TUNADEBUG
        Image_indexedToRGB(indexed_tmp, rgb_tmp);
        ImageToIplImage(rgb_tmp, ipl_out2);
        cvShowImage(out2, ipl_out2);
#endif

        continue;
        Image_colorFilter(indexed_tmp, indexed_tmp, &color, Util_max(colorFilterCount, 1));
        Image_toMonochrome(indexed_tmp, indexed_tmp);

#ifdef TUNADEBUG
        Image_indexedToRGB(indexed_tmp, rgb_tmp);
        ImageToIplImage(rgb_tmp, ipl_out3);
        cvShowImage(out3, ipl_out3);
#endif

        Image_identifyBlobs(indexed_tmp, indexed_tmp);

#ifdef TUNADEBUG
        Image_indexedToRGB(indexed_tmp, rgb_tmp);
        ImageToIplImage(rgb_tmp, ipl_out4);
        cvShowImage(out4, ipl_out4);
#endif
  
        printf("%5d\t%.3f\n", i++, Timer_getDelta(timer));
    }

    Timer_destroy(timer);

    Image_destroy(img_src);
    Image_destroy(rgb_tmp);
    Image_destroy(indexed_tmp);

#ifdef TUNADEBUG
    cvDestroyAllWindows();
#endif

    return 0;
}
