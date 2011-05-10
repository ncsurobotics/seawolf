/**
 * This is a recursive blob detection algorithm taken from seawolf's 2010 code,
 * which was originally created in the 2009 competition.
 */

#include <stdio.h>

#include <cv.h>
#include <highgui.h>

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

// Prototypes
int find_blobs(IplImage* Img, BLOB** blobs, int tracking_number, int minimum_blob_area);
BLOB* findPrimary(IplImage* Img, int target_number, int minimum_blob_area, int *blobs_found);
int checkPixel(IplImage* Img, int x, int y, unsigned int** pixlog, BLOB* blob, int depth); 
void blob_copy(BLOB* dest, BLOB* src);
void blob_free(BLOB* blobs, int blobs_found);

#define MAX_BLOB_AREA 50000

/** 
 * \ingroup blob
 * \{
 */

/**
 * \brief Finds blobs in an image.
 * This function is designed to be run on a color-filtered image.  It considers any NON-BLACK 
 * pixel to be of interest.  It sweeps the image for all clusters (blobs) of adjacent 
 * non-black pixels.  It then returns n largets blobs, where n is the tracking_number 
 *
 * Always free the output when you're done.  The proper way to free is to use the \ref blob_free function.
 *
 * Note! there is a hard-coded max blob size of 50,000 pixels to avoid stack errors.  
 * The recursive function also collapses at a depth of 100,000.  This has not been
 * observed to be a problem in any vision application
 *
 * Here is an example of the basic usage:
 * \code
 * BLOB *blobs; // The blobs will be stored here.
 * int number_of_blobs_found = blob(image, &blobs, 4, 100);
 * int area = blobs[0].area;
 * blob_free(blobs, number_of_blobs_found);
 * \endcode
 *
 * \param Img The binary image to find blobs in.
 * \param targets This double pointer will be filled will an array of
 *        blobs corresponding to the blob found in the image.
 * \param tracking_number The maximum number of blobs to find.  If more blobs
 *        are found, only the largest are kept.
 * \param minimum_blob_area Blobs with less than this many pixels are ignored.
 * \return The number of blobs found.
 *
 */
int find_blobs(IplImage* Img, BLOB** targets, int tracking_number, int minimum_blob_area) {
    if (Img->depth != 8) {
        printf("Error: find_blobs only accepts char type images.\n");
        return -1;
    }

    int blobnumber; // Holds the number of blobs we found

    // Find the most massive blobs and assign them to targets
    *targets = findPrimary(Img, tracking_number, minimum_blob_area, &blobnumber);

    int i;
    // Now compute the middle of each blob
    for(i=0;i<blobnumber;i++){
        (*targets)[i].mid.x = ((*targets)[i].left+(*targets)[i].right)/2;
        (*targets)[i].mid.y = ((*targets)[i].top + (*targets)[i].bottom)/2;
    }

    #ifdef VISION_LIB_BLOB
        IplImage* blob_pic = cvCreateImage(cvGetSize(Img),8,3);
        cvCopy(Img, blob_pic, 0);
        #ifdef VISION_GRAPHICAL
            cvNamedWindow("Blob", CV_WINDOW_AUTOSIZE);
        #endif
        int x,y;

        // Bind the blobs
        for(i=0; i<(blobnumber<tracking_number?blobnumber:tracking_number);i++){

            // Draw the top of the binding box
            uchar* ptr = (uchar*) (blob_pic->imageData + (*targets)[i].top * blob_pic->widthStep);
            for(x=(*targets)[i].left; x<=(*targets)[i].right;x++){
                ptr[Img->nChannels*x+0] = 0;
                ptr[Img->nChannels*x+1] = 254;
                ptr[Img->nChannels*x+2] = 0;
            }
            // Draw the bottom of the binding box
            ptr = (uchar*) (blob_pic->imageData + (*targets)[i].bottom * blob_pic->widthStep);
            for(x=(*targets)[i].left; x<=(*targets)[i].right;x++){
                ptr[Img->nChannels*x+0] = 0;
                ptr[Img->nChannels*x+1] = 254;
                ptr[Img->nChannels*x+2] = 0;
            }
            // Draw the left of the box
            for(y = (*targets)[i].top; y>= (*targets)[i].bottom; y--){
                ptr = (uchar*) (blob_pic->imageData + y * blob_pic->widthStep);
                x = (*targets)[i].left;
                ptr[Img->nChannels*x+0] = 0;
                ptr[Img->nChannels*x+1] = 254;
                ptr[Img->nChannels*x+2] = 0;
            }

            // Draw the left of the box
            for(y = (*targets)[i].top; y>= (*targets)[i].bottom; y--){
                ptr = (uchar*) (blob_pic->imageData + y * blob_pic->widthStep);
                x = (*targets)[i].right;
                ptr[Img->nChannels*x+0] = 0;
                ptr[Img->nChannels*x+1] = 254;
                ptr[Img->nChannels*x+2] = 0;
            }
        }

        #ifdef VISION_GRAPHICAL
            cvShowImage("Blob",blob_pic);
        #endif
        cvReleaseImage(&blob_pic);

    #endif

    return blobnumber;
}


/**
 * \brief Searches the image for the largest blob.
 * \private
 *
 * \param Img
 * \param tracking_number
 * \param minimum_blob_area
 * \param blobnumber
 * \return The blob found.
 */

BLOB* findPrimary(IplImage* Img, int tracking_number, int minimum_blob_area, int *blobnumber){

    //usefull variables
    int height = Img->height;
    int width = Img->width;
    int i,x,y;
    int blobs_found=0;

    //initialize an array of blobs
    BLOB* blobs;
    *blobnumber = 0; //how many blobs we've found so far

    //Allocate memory for blob variable
    blobs = (BLOB*)calloc(30000,sizeof(BLOB)); //30,000 is estimated max number of blobs

    //create a list of our target blobs, which we will combine into a single blob
    BLOB* targets;
    targets = (BLOB*)calloc(tracking_number,sizeof(BLOB));

    //create a list of targets if nto all blobs were requested
    if(tracking_number>0){
        //allocate memory for target pixels
        for(i=0;i<tracking_number;i++){
            targets[i].pixels = (CvPoint*)cvAlloc(MAX_BLOB_AREA*sizeof(CvPoint));
        }
    }

    unsigned int** pixlog;
    //Allocate array of pointers to keep track of pixels that have been checked
    pixlog = (unsigned int**)calloc(width,sizeof(unsigned int*));

    //Allocate the width dimention of the array of pointers to keep track of pixels that have been checked
    for(i=0; i<width; i++)
        pixlog[i] = (unsigned int*)calloc(height,sizeof(unsigned int));

    //now sweep the image looking for blobs (check a grid, not every pixel)
    for(y=0; y<height-3; y+=4 ) {
        uchar* ptr = (uchar*) (Img->imageData + y * Img->widthStep);
        for(x=0; x<width-3; x+=4 ) {
            //if the pixel hasn't been blacked out as the wrong color AND has not yet been checked
            if((ptr[Img->nChannels*x+0]||ptr[Img->nChannels*x+1]||ptr[Img->nChannels*x+2])&& pixlog[x][y]==0){
                //we've found a new blob, so let's initialize it's values
                blobs[*blobnumber].area = 0;
                blobs[*blobnumber].top = 0;
                blobs[*blobnumber].bottom = height;
                blobs[*blobnumber].right = 0;
                blobs[*blobnumber].left = width;
                blobs[*blobnumber].cent_x = 0;
                blobs[*blobnumber].cent_y = 0;
                blobs[*blobnumber].mid.x = 0;
                blobs[*blobnumber].mid.y = 0;
                blobs[*blobnumber].pixels = (CvPoint*)cvAlloc(sizeof(CvPoint)*MAX_BLOB_AREA);
                //now let's examine the blob and update it's properties
                int depth = 0;
                checkPixel(Img, x,y, pixlog, &blobs[*blobnumber], depth);

                //don't bother sorting if we are asked to return ALL the blobs (argument: tracking_number of zero)
                if(tracking_number > 0){
                    //now we check to see if this makes our list of top <tracking_number> biggest blobs
                    if(blobs[*blobnumber].area > targets[tracking_number-1].area && blobs[*blobnumber].area >= minimum_blob_area){
                        blobs_found++;

                        for(i = tracking_number-1; i >=0; i--){
                            if(blobs[*blobnumber].area <= targets[i].area){
                                blob_copy(&targets[i+1],&blobs[*blobnumber]);
                                i=-1;//we've found where it goes, don't come back into the loop
                            }
                            else if(i+1 < tracking_number){
                                blob_copy(&targets[i+1],&targets[i]);

                                //and for the case where this is the biggest blob
                                if(i==0){
                                    blob_copy(&targets[i],&blobs[*blobnumber]);
                                }
                            }
                        }
                    }
                }
                //increment blobnumber
                *blobnumber += 1;
            }
        }
    }

    //free the pixle log
    for(i=0; i<width; i++)
        free(pixlog[i]);
    free(pixlog);

    //if we want all the blobs, just return blobs and be done
    if(tracking_number == 0){
        return blobs;
    }
    blob_free(blobs,*blobnumber);

    //free the target pixels we don't need
    for(i=blobs_found;i<tracking_number;i++){
        cvFree(&targets[i].pixels);
    }

    //mark the size of targets
    *blobnumber = tracking_number < blobs_found? tracking_number:blobs_found;

    return targets;
}

/**
 * \brief Recursively called pixel-checking function of findprimary().
 * Examines an object pixel-by-pixel, checking each pixel to see if it
 * is the top bottom left or rightmost of the object. Then recursively calls
 * itself on all surrounding pixels that are part of the object. assignes total
 * number of pixels in the object to the object's area
 * \private
 */
 
int checkPixel(IplImage* Img, int x, int y, unsigned int** pixlog, BLOB* blob, int depth){

    //we will crash if we keep going, so let's just stop now
    if(++depth > 100000)
        return 1;

    if(pixlog[x][y] != 0)
        return 1; //we've checked this pixel, so shouldn't do it again
    //now mark this pixel as having been checked
    pixlog[x][y] = 1;

    //check too see if the pixel is part of the blob
    uchar* ptr = (uchar*) (Img->imageData + y * Img->widthStep);
    if((ptr[Img->nChannels*x+0] || ptr[Img->nChannels*x+1] || ptr[Img->nChannels*x+2]) == 0){
        return 2; //the pixel has been blacked out and shouldn't be used
    }

    int height = Img->height;
    int width = Img->width;

    //now that we know this is a new pixel belonging to the current blob, proccess it
    blob->area++; //increase area
    blob->cent_x = (blob->cent_x*(blob->area-1)+x)/(blob->area);
    blob->cent_y = (blob->cent_y*(blob->area-1)+y)/(blob->area);

    //quick saftey check. If the blob is ever this big the program no longer works, but at least this line keeps it from crashing
    if(blob->area >= MAX_BLOB_AREA)
        return 3;

    //now catagorize this pixel
    if(y > blob->top) blob->top = y;
    if(y < blob->bottom) blob->bottom = y;
    if(x < blob->left) blob->left = x;
    if(x > blob->right) blob->right = x;

    //add this pixel to the list for this blob
    blob->pixels[(blob->area-1)].x = x;
    blob->pixels[(blob->area-1)].y = y;
    //printf("pixels[%ld] being assigned {%d,%d}\n",blob->area-1,blob->pixels[(blob->area-1)].x,blob->pixels[(blob->area-1)].y);
    //fflush(NULL);

    int w,z;
    //now check all surrounding pixels
    for(w = x-1; w <= x+1; w++){
        for(z = y-1; z <= y+1; z++){
            //save from overfow
            if((w > 1)&&(z > 1)&&(w < width -1)&&(z < height-1))
                //now that we know we are on the image, check this pixel
                checkPixel(Img,w,z,pixlog, blob, depth);
        }
    }
    return 0;
}

/**
 * \brief copies contents of one BLOB structure to another
 * \private
 */
void blob_copy(BLOB* dest, BLOB* src){
    //copy src to destination
    dest->top   = src->top;
    dest->left  = src->left;
    dest->right = src->right;
    dest->bottom= src->bottom;
    dest->area  = src->area;
    dest->cent_x= src->cent_x;
    dest->cent_y= src->cent_y;
    dest->mid   = src->mid;
    memcpy(dest->pixels,src->pixels,MAX_BLOB_AREA*sizeof(CvPoint));
}

/**
 * \brief frees memory assigned by blob()
 *
 * \param blobs the array of BLOB elements to be freed
 * \param blobs_found the number of elements in that array
 */
 
void blob_free(BLOB* blobs, int blobs_found)
{
    int i;
    for(i=0;i<blobs_found;i++){
        cvFree(&blobs[i].pixels);
    }
    free(blobs);
}

/** \} */
