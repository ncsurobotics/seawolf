#ifndef __SEAWOLF_VISION_LIB_BLOB_INCLUDE_H
#define __SEAWOLF_VISION_LIB_BLOB_INCLUDE_H

typedef struct {
    int top; /**< Upper most pixel in the blob. */
    int left; /**< Left most pixel in the blob. */
    int right; /**< Right most pixel in the blob. */
    int bottom;  /**< Bottom most pixel in the blob. */
    long int area; /**< Area of the blob. */
    double cent_x; /**< X coordinate of the center of the blob */
    double cent_y; /**< Y coordinate of the center of the blob */
    CvPoint mid; /**< the centroid of the blob */
    CvPoint* pixels; /**< the pixels that compose the blob*/
} BLOB;

int blob(IplImage* Img, BLOB** blobs, int tracking_number, int minimum_blob_area);
BLOB* findPrimary(IplImage* Img, int target_number, int minimum_blob_area, int *blobs_found);
int checkPixel(IplImage* Img, int x, int y, unsigned int** pixlog, BLOB* blob, int depth); 
void blob_copy(BLOB* dest, BLOB* src);
void blob_free(BLOB* blobs, int blobs_found);

#endif
