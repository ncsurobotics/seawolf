
#include <seawolf.h>

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#include <cv.h>
#include <highgui.h>

//#define COMPARE 1
//#define VISUAL_DEBUG 1

#ifdef COMPARE

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
void blob_free(BLOB* blobs, int blobs_found);

#endif

#define BLOB_PART_TABLE_ALLOC_UNIT 256

#define UP_LEFT  0
#define UP       1
#define UP_RIGHT 2
#define LEFT     3

typedef struct Blob_s {
    uint32_t id;
    uint32_t c_x;
    uint32_t c_y;
    uint16_t size;
    uint8_t keep;
} Blob;

typedef struct BlobPart_s {
    Blob* blob;
    struct BlobPart_s* next;
    struct BlobPart_s* prev;
    uint16_t part_size;
    uint16_t stored;
} BlobPart;

static void join_blob_parts(BlobPart** parts, uint32_t i, uint32_t j);

static void join_blob_parts(BlobPart** parts, uint32_t i, uint32_t j) {
    BlobPart* tail = parts[i];
    BlobPart* head = parts[j];
    Blob* blob = parts[i]->blob;

    while(tail->next) {
        tail = tail->next;
    }

    while(head->prev) {
        head = head->prev;
    }

    tail->next = head;
    head->prev = tail;

    tail->blob->size += head->blob->size;

    while(head) {
        head->blob = blob;
        head = head->next;
    }
}

void free_blobs(Blob** blobs, int num_blobs) {
    for(int i = 0; i < num_blobs; i++) {
        free(blobs[i]);
    }
    free(blobs);
}

int find_blobs2(IplImage* img_in, IplImage* blobs_out, Blob*** blobs, int min_size, int keep_number) {
    uint32_t blob_part_table_size = BLOB_PART_TABLE_ALLOC_UNIT;
    BlobPart** blob_parts = calloc(sizeof(BlobPart*), blob_part_table_size);

    uint32_t* blob_mapping = calloc(sizeof(uint32_t), img_in->height * img_in->widthStep);
    uint32_t* pixel_above = blob_mapping - img_in->widthStep;
    uint8_t* img_pixel = (uint8_t*) img_in->imageData;
    uint32_t* map_pixel = blob_mapping;

    uint32_t next_part_id = 1;
    
    uint32_t row = 0;
    uint32_t column = 0;

    int32_t adjacent_parts[4];
    int32_t assigned_to;
    Blob* target_blob;

    uint8_t row_padding = img_in->widthStep - img_in->width;

    uint32_t num_blobs = 0;

    List* raw_blobs = List_new();

    int i;

    blob_parts[0] = calloc(sizeof(BlobPart), BLOB_PART_TABLE_ALLOC_UNIT);
    for(i = 1; i < BLOB_PART_TABLE_ALLOC_UNIT; i++) {
        blob_parts[i] = &blob_parts[0][i];
    }

    for(row = 0; row < img_in->height; row++) {
        for(column = 0; column < img_in->width; column++) {
            memset(adjacent_parts, 0, sizeof(adjacent_parts));
            
            if(*img_pixel) {
                /* Build list of adjacent blob parts */
                if(row > 0) {
                    if(column > 0) {
                        adjacent_parts[UP_LEFT] = pixel_above[-1];
                    }
                    
                    adjacent_parts[UP] = pixel_above[0];
                    
                    if(column < img_in->width - 1) {
                        adjacent_parts[UP_RIGHT] = pixel_above[1];
                    }
                    
                }
                if(column > 0) {
                    adjacent_parts[LEFT] = *(map_pixel - 1);
                }

            
                /* Scan the list of adjacent pixel parts for the one with the lowest index */
                assigned_to = 0;
                for(i = 0; i < 4; i++) {
                    if(adjacent_parts[i]) {
                        assigned_to = adjacent_parts[i++];
                        break;
                    }
                }
            
                /* No adjacent blob pixels, create new blob part */
                if(assigned_to == 0) {
                    assigned_to = next_part_id;

                    blob_parts[assigned_to]->blob = calloc(sizeof(Blob), 1);
                    blob_parts[assigned_to]->blob->keep = true;
                    List_append(raw_blobs, blob_parts[assigned_to]->blob);
                    next_part_id++;

                    if(next_part_id >= blob_part_table_size) {
                        blob_parts = realloc(blob_parts, sizeof(BlobPart*) * (blob_part_table_size + BLOB_PART_TABLE_ALLOC_UNIT));
                        blob_parts[blob_part_table_size] = calloc(sizeof(BlobPart), BLOB_PART_TABLE_ALLOC_UNIT);

                        for(i = 1; i < BLOB_PART_TABLE_ALLOC_UNIT; i++) {
                            blob_parts[blob_part_table_size + i] = &blob_parts[blob_part_table_size][i];
                        }
                    
                        blob_part_table_size += BLOB_PART_TABLE_ALLOC_UNIT;
                        i = 4;
                    }
                }
            
                /* Store blob part identifier */
                blob_parts[assigned_to]->part_size++;
                blob_parts[assigned_to]->blob->size++;
                (*map_pixel) = assigned_to;
                target_blob = blob_parts[assigned_to]->blob;

                /* Connect newly adjacent blob parts */
                while(i < 4) {
                    if(adjacent_parts[i] && blob_parts[adjacent_parts[i]]->blob != target_blob) {
                        //List_remove(raw_blobs, List_indexOf(raw_blobs, blob_parts[adjacent_parts[i]]->blob));
                        blob_parts[adjacent_parts[i]]->blob->keep = false;

                        /* Join the blobs, assigning the blob parts in
                           adjacent_parts[j] to the blob in assigned_to */
                        join_blob_parts(blob_parts, assigned_to, adjacent_parts[i]);
                    }
                    
                    i++;
                }
            }

            pixel_above++;
            map_pixel++;
            img_pixel++;
        }

        pixel_above += row_padding;
        map_pixel += row_padding;
        img_pixel += row_padding;
    }

    printf("Blob parts: %d\n", next_part_id);

    int raw_blobs_count = List_getSize(raw_blobs);
    Blob* b;
    int j, k;

    (*blobs) = malloc(sizeof(Blob*) * keep_number);

    Timer* timer = Timer_new();

    i = 0;
    for(j = 0; j < raw_blobs_count; j++) {
        b = List_get(raw_blobs, j);

        if(b->keep == false) {
            continue;
        }

        if(b->size < min_size) {
            continue;
        }

        k = 0;
        while(k < i && b->size < (*blobs)[k]->size) {
            k++;
        }

        memmove((*blobs) + k + 1, (*blobs) + k, (i - k) * sizeof(Blob**));
        (*blobs)[k] = b;

        i++;
        if(i >= keep_number) {
            break;
        }
    }

    num_blobs = i;

    for(j = j + 1; j < raw_blobs_count; j++) {
        b = List_get(raw_blobs, j);

        if(b->keep == false) {
            continue;
        }

        if(b->size < min_size) {
            continue;
        }

        if(b->size <= (*blobs)[keep_number - 1]->size) {
            continue;
        }

        i = 0;
        while(b->size < (*blobs)[i]->size) {
            i++;
        }

        memmove((*blobs) + i + 1, (*blobs) + i, (keep_number - i - 1) * sizeof(Blob**));
        (*blobs)[i] = b;
    }

    printf("%.4f\n", Timer_getDelta(timer));

    for(i = 0; i < num_blobs; i++) {
        (*blobs)[i]->id = i + 1;
    }

    map_pixel = blob_mapping;
    img_pixel = (uint8_t*) blobs_out->imageData;

    /* Write out the real blob ids */
    for(row = 0; row < blobs_out->height; row++) {
        for(column = 0; column < blobs_out->width; column++) {
            if((*map_pixel)) {
                (*img_pixel) = blob_parts[*map_pixel]->blob->id;
            } else {
                (*img_pixel) = 0;
            }

            map_pixel++;
            img_pixel++;
        }
        
        map_pixel += row_padding;
        img_pixel += row_padding;
    }

    for(i = 0; i < blob_part_table_size; i += BLOB_PART_TABLE_ALLOC_UNIT) {
        free(blob_parts[i]);
    }
    free(blob_parts);
    free(blob_mapping);
    
    for(i = 0; i < raw_blobs_count; i++) {
        b = List_get(raw_blobs, i);
        if(b->id == 0) {
            free(b);
        }
    }
    List_destroy(raw_blobs);

    return num_blobs;
}

int main(int argc, char** argv) {
    // CvCapture* camera = cvCaptureFromCAM(0);
    IplImage* img_in = cvLoadImage(argv[1], CV_LOAD_IMAGE_GRAYSCALE); // = cvQueryFrame(camera);
    IplImage* binary = cvCreateImage(cvGetSize(img_in), 8, 1);
    IplImage* binary2 = cvCreateImage(cvGetSize(img_in), 8, 1);

    int value1 = 15, value2 = 20, min_blob = 512, most_blobs = 64;

    Timer* timer = Timer_new();

    Blob** blobs;
    int num_blobs;

#ifdef COMPARE
    BLOB* other_blobs;
#endif

#ifdef VISUAL_DEBUG
    //    cvNamedWindow("original", CV_WINDOW_AUTOSIZE);
    cvNamedWindow("binary", CV_WINDOW_AUTOSIZE);
    cvNamedWindow("binary2", CV_WINDOW_AUTOSIZE);

    cvCreateTrackbar("value1", "binary", &value1, 15, NULL);
    cvCreateTrackbar("value2", "binary", &value2, 20, NULL);
    cvCreateTrackbar("minblob", "binary", &min_blob, 512, NULL);
    cvCreateTrackbar("mostblobs", "binary", &most_blobs, 4096, NULL);

#endif

    while(true) {
        // img_in = cvQueryFrame(camera);
        // cvCvtColor(img_in, binary, CV_RGB2GRAY);
        // cvShowImage("original", binary);
        cvSmooth(img_in, binary, CV_GAUSSIAN, 5, 5, 0, 0);
        cvAdaptiveThreshold(binary, binary, 255, CV_ADAPTIVE_THRESH_MEAN_C, CV_THRESH_BINARY_INV, value1, value2);
        
#ifdef VISUAL_DEBUG
        cvShowImage("binary", binary);
#endif

        Timer_reset(timer);
        num_blobs = find_blobs2(binary, binary2, &blobs, min_blob, most_blobs);
        printf("blobs2: %5.3f\n\n", Timer_getDelta(timer));
        printf("Found %d blobs\n", num_blobs);
        free_blobs(blobs, num_blobs);


#ifdef COMPARE
        Timer_reset(timer);
        num_blobs = find_blobs(binary, &other_blobs, most_blobs, min_blob);
        blob_free(other_blobs, num_blobs);
        printf("blobs: %5.3f\n", Timer_getDelta(timer));
#endif

#ifdef VISUAL_DEBUG
        cvShowImage("binary2", binary2);
        if(cvWaitKey(-1) == 'q') break;
#else
        break;
#endif
    }

    cvReleaseImage(&img_in);
    cvReleaseImage(&binary);
    cvReleaseImage(&binary2);
#ifdef VISUAL_DEBUG
    cvDestroyAllWindows();
#endif

    Timer_destroy(timer);
    
    return 0;
}
