
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

/* Number of BlobPart structures to allocate at once */
#define BLOB_PART_TABLE_ALLOC_UNIT 256

/* Indexes into the adjacency table. These are positions relative to the current
   input pixel */
#define UP_LEFT  0
#define UP       1
#define UP_RIGHT 2
#define LEFT     3

typedef uint32_t BlobPartId;
typedef uint32_t BlobId;

typedef struct Blob_s {
    BlobId id;

    /* If size == -1 then the blob is no longer valid. This is set when two
       blobs are joined. Otherwise, this gives the size of the blob in pixels */
    int32_t size;

    /* Centroid */
    uint32_t c_x;
    uint32_t c_y;

    /* Bound box */
    uint16_t x_0;
    uint16_t x_1;
    uint16_t y_0;
    uint16_t y_1;
} Blob;

typedef struct BlobPart_s {
    Blob* blob;
    struct BlobPart_s* next;
    struct BlobPart_s* prev;
} BlobPart;

static void join_blob_parts(BlobPart** parts, BlobPartId i, BlobPartId j);

static void join_blob_parts(BlobPart** parts, BlobPartId i, BlobPartId j) {
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
    head->blob->size = -1;

    while(head) {
        head->blob = blob;
        head = head->next;
    }
}

static BlobPart** grow_blob_parts_table(BlobPart** parts, size_t* current_size) {
    size_t old_size = *current_size;
    size_t new_size = old_size + BLOB_PART_TABLE_ALLOC_UNIT;

    parts = realloc(parts, sizeof(BlobPart*) * new_size);
    parts[old_size] = calloc(sizeof(BlobPart), BLOB_PART_TABLE_ALLOC_UNIT);

    for(int i = 1; i < BLOB_PART_TABLE_ALLOC_UNIT; i++) {
        parts[old_size + i] = &(parts[old_size][i]);
    }
    
    (*current_size) = new_size;

    return parts;
}

/**
 * \brief Locate contigous regions (blobs) in a binary imgae
 *
 * Locates blobs in an input image. The input image is considered as binary,
 * where a pixel value of 0 is considered black, and anything else white. This
 * function finds all contiguous regions (blobs) of white pixels meeting the
 * given specifications. The minimum blob size to accept can be given, and the
 * maximum number of blobs to return. If the image contains more blobs than the
 * number desired, then the largest are returned. Each blob has a unique id and
 * this id is used to index the output image. Pixels in returned blobs have
 * their values set to their blob's index. All other pixels are set to 0. No
 * blob is given an id of 0.
 *
 * The returned list of blobs gives the id, size, center of mass, and bounding
 * box for each blob. The returned blob list can be freed using free_blobs.
 *
 * \param img_in The input image. Should be single channel, 8 bit depth
 * \param img_out The indexed output image. Should be single channel, 8 bit depth
 * \param r_num_blobs A pointer to an integer where the number of blobs returned can be stored
 * \param min_size Any blobs smaller than this will be discarded
 * \param keep_number Maximum number of blobs to return
 * \param out_coloring Color pixels in output map. If 0 is given then blob ids determine color
 * \return A list of blobs
 */
Blob** find_blobs(IplImage* img_in, IplImage* blobs_out, int* r_num_blobs, int min_size, int keep_number, uint8_t out_coloring) {
    size_t blob_part_table_size = 0;
    BlobPart** blob_parts = NULL;

    BlobPartId* blob_mapping = calloc(sizeof(BlobPartId), img_in->height * img_in->widthStep);

    BlobPartId* pixel_above = blob_mapping - img_in->widthStep;
    BlobPartId* map_pixel = blob_mapping;
    uint8_t* img_pixel = (uint8_t*) img_in->imageData;
    uint8_t row_padding = img_in->widthStep - img_in->width;
    
    BlobPartId next_part_id = 1;
    BlobPartId adjacent_parts[4];
    BlobPartId assigned_to;

    /* Blobs as their created. This includes "decommissioned" blobs */
    List* raw_blobs = List_new();
    int num_raw_blobs = 0;

    /* Blobs that we return. May be less than keep_number, but the memories
       cheaper than the CPU cycles */
    Blob** blobs = malloc(sizeof(Blob*) * keep_number);
    int num_blobs = 0;

    uint32_t row, column;
    uint32_t height = img_in->height;
    uint32_t width = img_in->width;

    Blob* b;
    int i, j;

    /* Go through the input image and construct all the blob parts and raw blobs */
    for(row = 0; row < height; row++) {
        for(column = 0; column < width; column++) {
            memset(adjacent_parts, 0, sizeof(adjacent_parts));
            
            if(*img_pixel) {
                /* Build list of adjacent blob parts */
                if(row > 0) {
                    if(column > 0) {
                        adjacent_parts[UP_LEFT] = pixel_above[-1];
                        adjacent_parts[LEFT] = *(map_pixel - 1);
                    }
                    
                    adjacent_parts[UP] = pixel_above[0];
                    
                    if(column < width - 1) {
                        adjacent_parts[UP_RIGHT] = pixel_above[1];
                    }
                } else if(column > 0) {
                    adjacent_parts[LEFT] = *(map_pixel - 1);
                }
            
                /* Find the first adjacency */
                assigned_to = 0;
                for(i = 0; i < 4; i++) {
                    if(adjacent_parts[i]) {
                        assigned_to = adjacent_parts[i];
                        break;
                    }
                }
            
                /* No adjacent blob pixels, create new blob part */
                if(assigned_to == 0) {
                    assigned_to = next_part_id;

                    /* Grow BlobParts table if there's no free space */
                    if(assigned_to >= blob_part_table_size) {
                        blob_parts = grow_blob_parts_table(blob_parts, &blob_part_table_size);
                    }

                    /* Create the new blob */
                    b = calloc(sizeof(Blob), 1);

                    List_append(raw_blobs, b);
                    blob_parts[assigned_to]->blob = b;
                    
                    next_part_id++;
                    num_raw_blobs++;
                }
            
                /* Store blob part identifier */
                (*map_pixel) = assigned_to;

                b = blob_parts[assigned_to]->blob;
                b->size++;

                /* Connect newly adjacent blob parts */
                for(i = i + 1; i < 4; i++) {
                    if(adjacent_parts[i] && blob_parts[adjacent_parts[i]]->blob != b) {
                        /* Join the blobs, assigning the blob parts in
                           adjacent_parts[j] to the blob in assigned_to */
                        join_blob_parts(blob_parts, assigned_to, adjacent_parts[i]);
                    }
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

    /* Generate the sorted list of blobs we're keeping. This is done by going
       through all the raw blobs and when one is found that's bigger than the
       smallest one we've already selected, we remove the smallest one and add
       the new one into the list so that the list of blobs to keep stays
       ordered. */
    for(i = 0; i < num_raw_blobs; i++) {
        b = List_get(raw_blobs, i);

        if(b->size < min_size) {
            continue;
        }

        /* If we've found keep_number of blobs already and this one is smaller
           than our current smallest, then skip it */
        if(num_blobs == keep_number && b->size <= blobs[num_blobs - 1]->size) {
            continue;
        }

        /* Find the place in the sorted list this blob should go */
        j = 0;
        while(j < num_blobs && b->size < blobs[j]->size) {
            j++;
        }

        /* If there's already a blob where this one should go then move all the
           ones after it down by one */
        if(num_blobs == keep_number) {
            memmove(blobs + j + 1, blobs + j, (num_blobs - j - 1) * sizeof(Blob*));
        } else {
            memmove(blobs + j + 1, blobs + j, (num_blobs - j) * sizeof(Blob*));
        }
        blobs[j] = b;

        /* Increment the number of blobs if we don't already have the maximum number */
        if(num_blobs < keep_number) {
            num_blobs++;
        }
    }

    /* Assigned blob ids to the blobs we are keeping and initialize boundings
       boxes. Remember, id 0 is reserved so we don't use it here */
    for(i = 0; i < num_blobs; i++) {
        b = blobs[i];
        b->id = i + 1;

        /* Set bounding box to extreme values before hand */
        b->x_0 = img_in->width;
        b->x_1 = 0;
        b->y_0 = img_in->height;
        b->y_1 = 0;

        /* Zero the accumulators for the centroid calculation */
        b->c_x = 0;
        b->c_y = 0;
    }

    map_pixel = blob_mapping;
    img_pixel = (uint8_t*) blobs_out->imageData;

    /* Write out the output image and compute blob bounding boxes/regions of
       interest and blob centroids */
    for(row = 0; row < height; row++) {
        for(column = 0; column < width; column++) {
            if((*map_pixel)) {
                b = blob_parts[*map_pixel]->blob;

                /* Save the blob id to the output image (this may be 0, but
                   we're not keeping blobs with id 0 anyway) */
                (*img_pixel) = b->id;

                if(b->id) {
                    /* If a static coloring is being used rewrite the pixel value */
                    if(out_coloring) {
                        (*img_pixel) = out_coloring;
                    }
                    
                    /* Running totals of x, y pixel locations in this
                       blob. These are divided by the blob size in the end to
                       get the blob's center of mass */
                    b->c_x += column;
                    b->c_y += row;

                    /* Update the bounds on the bounding box as necessary */
                    if(column < b->x_0) {
                        b->x_0 = column;
                    }

                    if(column > b->x_1) {
                        b->x_1 = column;
                    }

                    if(row < b->y_0) {
                        b->y_0 = row;
                    }

                    if(row > b->y_1) {
                        b->y_1 = row;
                    }

                }
            } else {
                (*img_pixel) = 0;
            }

            map_pixel++;
            img_pixel++;
        }
        
        map_pixel += row_padding;
        img_pixel += row_padding;
    }

    /* Divide c_x, c_y by size to give the center of mass of the blob */
    for(i = 0; i < num_blobs; i++) {
        blobs[i]->c_x /= blobs[i]->size;
        blobs[i]->c_y /= blobs[i]->size;
    }

    /* Free each chunk of blob part */    
    for(i = 0; i < blob_part_table_size; i += BLOB_PART_TABLE_ALLOC_UNIT) {
        free(blob_parts[i]);
    }

    free(blob_parts);
    free(blob_mapping);

    /* Free any blobs that aren't being returned */
    for(i = 0; i < num_raw_blobs; i++) {
        b = List_get(raw_blobs, i);
        if(b->id == 0) {
            free(b);
        }
    }

    /* Destroy the list of raw blobs */
    List_destroy(raw_blobs);

    /* Save the number of blobs and return the blobs list */
    (*r_num_blobs) = num_blobs;
    return blobs;
}

/**
 * \brief Free blobs returned by find_blobs
 *
 * Free resources returned by find_blobs
 *
 * \param blobs List of pointers to Blob structures as returned by find_blobs.
 * \param num_blobs Number of Blobs in blobs
 */
void free_blobs(Blob** blobs, int num_blobs) {
    for(int i = 0; i < num_blobs; i++) {
        free(blobs[i]);
    }
    free(blobs);
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

/* Wrapper around find_blobs which takes Python IplImages (a.k.a PyObject) and
   calls find_blobs with the underlying IplImage structures */
Blob** _wrap_find_blobs(struct iplimage_t* _img_in, struct iplimage_t* _blobs_out, int* r_num_blobs, int min_size, int keep_number, int out_coloring) {
    return find_blobs(_img_in->a, _blobs_out->a, r_num_blobs, min_size, keep_number, (uint8_t) out_coloring);
}

#endif // #ifdef __SW_LIBVISION
