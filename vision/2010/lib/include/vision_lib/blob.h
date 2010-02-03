#ifndef __SEAWOLF_VISION_LIB_BLOB_INCLUDE_H
#define __SEAWOLF_VISION_LIB_BLOB_INCLUDE_H

typedef struct {
    int top;
    int left;
    int right;
    int bottom; 
    long int area;
    double cent_x;
    double cent_y;
    CvPoint mid;
    CvPoint* pixels; 
} BLOB;

void blob_init();
int blob(IplImage* Img, BLOB** blobs, int tracking_number, int minimum_blob_area);
BLOB* findPrimary(IplImage* Img, int target_number, int minimum_blob_area, int *blobs_found);
int checkPixel(IplImage* Img, int x, int y, unsigned int** pixlog, BLOB* blob, int depth); 
void blob_copy(BLOB* dest, BLOB* src);
//void blob_free(BLOB* blob, int blobs_found);
void blob_free();

#endif
