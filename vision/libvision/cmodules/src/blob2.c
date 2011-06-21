
#include <seawolf.h>
#include <cv.h>
#include <highgui.h>

#include <stdbool.h>
#include <stdint.h>

#include <Python.h>

#define BLOB_PART_TABLE_ALLOC_UNIT 256

#define UP_LEFT  0
#define UP       1
#define UP_RIGHT 2
#define LEFT     3

struct iplimage_t {
  PyObject_HEAD
  IplImage *a;
  PyObject *data;
  size_t offset;
};

typedef struct Blob_s {
    uint32_t id;
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
    head->blob->size = -1;

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

Blob** find_blobs(IplImage* img_in, IplImage* blobs_out, int* r_num_blobs, int min_size, int keep_number) {
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

    List* raw_blobs = List_new();

    Blob** blobs = NULL;
    int num_blobs;

    Blob* b;
    int i, j, k;

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

    int raw_blobs_count = List_getSize(raw_blobs);

    blobs = malloc(sizeof(Blob*) * keep_number);

    i = 0;
    for(j = 0; j < raw_blobs_count; j++) {
        b = List_get(raw_blobs, j);

        if(b->size < min_size) {
            continue;
        }

        k = 0;
        while(k < i && b->size < blobs[k]->size) {
            k++;
        }

        memmove(blobs + k + 1, blobs + k, (i - k) * sizeof(Blob*));
        blobs[k] = b;

        i++;
        if(i >= keep_number) {
            break;
        }
    }

    num_blobs = i;

    for(j = j + 1; j < raw_blobs_count; j++) {
        b = List_get(raw_blobs, j);

        if(b->size < min_size) {
            continue;
        }

        if(b->size <= blobs[num_blobs - 1]->size) {
            continue;
        }

        i = 0;
        while(b->size < blobs[i]->size) {
            i++;
        }

        memmove(blobs + i + 1, blobs + i, (keep_number - i - 1) * sizeof(Blob*));
        blobs[i] = b;
    }

    for(i = 0; i < num_blobs; i++) {
        blobs[i]->id = i + 1;

        /* Set bounding box to extreme values before hand */
        blobs[i]->x_0 = img_in->width;
        blobs[i]->x_1 = 0;
        blobs[i]->y_0 = img_in->height;
        blobs[i]->y_1 = 0;
    }

    map_pixel = blob_mapping;
    img_pixel = (uint8_t*) blobs_out->imageData;

    /* Write out the real blob ids */
    for(row = 0; row < blobs_out->height; row++) {
        for(column = 0; column < blobs_out->width; column++) {
            if((*map_pixel)) {
                b = blob_parts[*map_pixel]->blob;
                (*img_pixel) = b->id;

                if(b->id) {
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

                    b->c_x += column;
                    b->c_y += row;
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

    (*r_num_blobs) = num_blobs;
    return blobs;
}

Blob** _wrap_find_blobs(struct iplimage_t* _img_in, struct iplimage_t* _blobs_out, int* r_num_blobs, int min_size, int keep_number) {
    return find_blobs(_img_in->a, _blobs_out->a, r_num_blobs, min_size, keep_number);
}
