
#include <seawolf.h>

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#include <cv.h>
#include <highgui.h>

//#define COMPARE 1
#define VISUAL_DEBUG 1

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

typedef struct BlobPart_s {
    uint16_t blob_id;
    uint16_t part_size;
    uint16_t stored;
    struct BlobPart_s* next;
    struct BlobPart_s* prev;
} BlobPart;

typedef struct Blob_s {
    uint8_t keep;
    uint16_t size;
    uint32_t c_x;
    uint32_t c_y;
} Blob;

static void join_blob_parts(BlobPart** parts, uint32_t i, uint32_t j);
static inline bool is_same_blob(BlobPart** parts, uint32_t i, uint32_t j);
static void build_blob(Blob* blob, uint16_t blob_id, BlobPart* part);
static Blob* build_blobs_list(BlobPart** parts, uint32_t num_parts, uint32_t *num_blobs);

static void join_blob_parts(BlobPart** parts, uint32_t i, uint32_t j) {
    BlobPart* tail = parts[i];
    BlobPart* head = parts[j];
    uint32_t blob_id = parts[i]->blob_id;

    while(tail->next) {
        tail = tail->next;
    }

    while(head->prev) {
        head = head->prev;
    }

    tail->next = head;
    head->prev = tail;

    while(head) {
        head->blob_id = blob_id;
        head = head->next;
    }
}

static inline bool is_same_blob(BlobPart** parts, uint32_t i, uint32_t j) {
    return parts[i]->blob_id == parts[j]->blob_id;
}

/**
 * Given an uninitialized Blob structure, a blob id, and one part of the blob
 * reassign all blob_id's of the parts and compute the size of the blob 
 */
static void build_blob(Blob* blob, uint16_t blob_id, BlobPart* part) {
    blob->keep = false;
    blob->c_x = 0;
    blob->c_y = 0;

    while(part->prev) {
        part = part->prev;
    }

    blob->size = 0;
    while(part) {
        blob->size += part->part_size;
        part->blob_id = blob_id;
        part->stored = 1;
        part = part->next;
    }
}

static Blob* build_blobs_list(BlobPart** parts, uint32_t num_parts, uint32_t *num_blobs) {
    uint16_t max_id = 256;
    uint16_t blob_id = 0;
    Blob* blobs = calloc(sizeof(Blob), max_id);

    for(int i = 0; i < num_parts; i++) {
        /* Check if blob part alread assigned */
        if(parts[i]->stored) {
            continue;
        }
        
        build_blob(&blobs[blob_id], blob_id, parts[i]);

        blob_id++;
        if(blob_id >= max_id) {
            max_id += 16;
            blobs = realloc(blobs, sizeof(Blob) * max_id);
        }
    }

    (*num_blobs) = blob_id;
    return blobs;
}

static bool add_largest_blob(Blob* blobs, uint32_t num_blobs, int min_size) {
    int largest_i = 0;

    while(blobs[largest_i].keep == true) {
        largest_i++;
    }

    for(int i = largest_i + 1; i < num_blobs; i++) {
        if(blobs[i].keep == false && blobs[i].size > blobs[largest_i].size) {
            largest_i = i;
        }
    }

    if(blobs[largest_i].size < min_size) {
        return false;
    }

    blobs[largest_i].keep = true;
    return true;
}

static int filter_blob_list(Blob* blobs, uint32_t num_blobs, int min_size, int keep) {
    int i;

    if(num_blobs < keep) {
        keep = num_blobs;
        for(i = 0; i < num_blobs; i++) {
            if(blobs[i].size > min_size) {
                blobs[i].keep = true;
            } else {
                keep--;
            }
        }
    } else {
        for(i = 0; i < keep; i++) {
            if(add_largest_blob(blobs, num_blobs, min_size) == false) {
                return i;
            }
        }
    }

    return keep;
}

int find_blobs2(IplImage* img_in, IplImage* blobs_out, int min_size, int keep_number) {
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
    uint16_t target_blob;

    uint8_t row_padding = img_in->widthStep - img_in->width;

    Blob* blobs = NULL;
    uint32_t num_blobs;

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
                    adjacent_parts[LEFT] = blob_mapping[i - 1];
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

                    blob_parts[assigned_to]->blob_id = assigned_to;
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
                *map_pixel = assigned_to;
                target_blob = blob_parts[assigned_to]->blob_id;

                /* Connect newly adjacent blob parts */
                while(i < 4) {
                    if(adjacent_parts[i] && blob_parts[adjacent_parts[i]]->blob_id != target_blob) {
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

    blobs = build_blobs_list(blob_parts, next_part_id, &num_blobs);
    filter_blob_list(blobs, num_blobs, min_size, keep_number);

    
    map_pixel = blob_mapping;
    img_pixel = (uint8_t*) blobs_out->imageData;

    /* Write out the real blob ids */
    for(row = 0; row < blobs_out->height; row++) {
        for(column = 0; column < blobs_out->width; column++) {
            if((*map_pixel) && blobs[blob_parts[(*map_pixel)]->blob_id].keep) {
                (*img_pixel) = (blob_parts[*map_pixel]->blob_id % 255) + 1;
            } else {
                (*img_pixel) = 0;
            }

            map_pixel++;
            img_pixel++;
        }
        
        map_pixel += row_padding;
        img_pixel += row_padding;
    }

    free(blobs);
    free(blob_mapping);
    
    for(i = 0; i < blob_part_table_size; i += BLOB_PART_TABLE_ALLOC_UNIT) {
        free(blob_parts[i]);
    }
    free(blob_parts);

    return num_blobs;
}

int main(int argc, char** argv) {
    IplImage* img_in = cvLoadImage(argv[1], CV_LOAD_IMAGE_GRAYSCALE);
    IplImage* binary = cvCreateImage(cvGetSize(img_in), 8, 1);
    IplImage* binary2 = cvCreateImage(cvGetSize(img_in), 8, 1);

    int value1 = 15, value2 = 20, min_blob = 25, most_blobs = 10;

    Timer* timer = Timer_new();

#ifdef COMPARE
    BLOB* blobs;
    int num_blobs;
#endif

#ifdef VISUAL_DEBUG
    cvNamedWindow("original", CV_WINDOW_AUTOSIZE);
    cvNamedWindow("binary", CV_WINDOW_AUTOSIZE);
    cvNamedWindow("binary2", CV_WINDOW_AUTOSIZE);

    cvCreateTrackbar("value1", "binary", &value1, 15, NULL);
    cvCreateTrackbar("value2", "binary", &value2, 20, NULL);
    cvCreateTrackbar("minblob", "binary", &min_blob, 512, NULL);
    cvCreateTrackbar("mostblobs", "binary", &most_blobs, 4096, NULL);

    cvShowImage("original", img_in);
#endif

    while(true) {
        cvSmooth(img_in, binary, CV_GAUSSIAN, 5, 5, 0, 0);
        cvAdaptiveThreshold(binary, binary, 255, CV_ADAPTIVE_THRESH_MEAN_C, CV_THRESH_BINARY_INV, value1, value2);
        
#ifdef VISUAL_DEBUG
        cvShowImage("binary", binary);
#endif

        Timer_reset(timer);
        printf("Found %d blobs\n", find_blobs2(binary, binary2, min_blob, most_blobs));
        printf("blobs2: %5.3f\n", Timer_getDelta(timer));

#ifdef COMPARE
        Timer_reset(timer);
        num_blobs = find_blobs(binary, &blobs, most_blobs, min_blob);
        blob_free(blobs, num_blobs);
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
