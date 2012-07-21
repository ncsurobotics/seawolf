
/**
 * \file blob2.c
 * \brief New find_blobs routine
 *
 * Algorithm:
 *
 * A first pass is made through the image. As pixels are found they are added
 * to BlobParts. If any of the 4 pixels surrounding the pixel, which have
 * already been visited already belong to a BlobPart, the pixel is added to one
 * of these exists BlobParts. Otherwise, the pixel is added to a new
 * BlobPart. BlobParts are parts of Blobs, with each BlobPart belonging to a
 * single blob. When a pixel is found to be adjacent to two other pixels which
 * belong to different BlobParts and Blobs, these Blobs are joined together into
 * one blob.
 *
 * Internally, the relationships between BlobParts which belong to the same Blob
 * are represented by a linked list. BlobParts which belong to the same Blob are
 * part of the same BlobParts chain. When two Blobs are combined, the BlobParts
 * chains are joined head to tail and the BlobParts of one join the Blob of the
 * other.
 *
 * Now a mapping of pixels to BlobParts has been established, and all
 * BlobParts point to their Blobs. At this point the list of Blobs is filtered,
 * and the blob indexes written to the output image.
 */

#include <seawolf.h>
#include <cv.h>

#include <stdint.h>

#ifdef __SW_LIBVISION
# include <Python.h>
#endif

void greymap(IplImage* img_in, IplImage* img_out, uint8_t map[256]) {
    uint8_t row_padding = img_in->widthStep - img_in->width;
    int i = 0;

    for(int x = 0; x < img_in->width; x++) {
        for(int y = 0; y < img_in->height; y++) {
            img_out->imageData[i] = map[(uint8_t)img_in->imageData[i]];
            i++;
        }

        i += row_padding;
    }
}

#ifdef __SW_LIBVISION

/***************************************
 ******  Python abstraction layer ******
 ***************************************/

/* Representation of OpenCV IplImage within Python. Pulled from OpenCV Python
   interface code (modules/python/cv.cpp) */
struct iplimage_t {
  PyObject_HEAD
  IplImage *a;
  PyObject *data;
  size_t offset;
};

void _wrap_greymap(struct iplimage_t* _img_in, struct iplimage_t* _img_out, uint8_t _map[256]) {
    greymap(_img_in->a, _img_out->a, _map);
}

#endif // #ifdef __SW_LIBVISION
