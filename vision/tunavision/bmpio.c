
#include "img.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* These functions support the 54 byte V3 BMP format described at
   http://en.wikipedia.org/wiki/BMP_file_format
 */

Image* Bitmap_read(const char* path) {
    /* Header information */
    unsigned char magic_num[2];
    unsigned int data_offset;
    unsigned int dib_size;
    unsigned int width, height;
    unsigned short depth;
    unsigned int compression;

    /* Calculated value */
    unsigned int data_width;
    size_t pixel_size;
    size_t row_size;

    /* Buffer for rows */
    unsigned char* row_buffer;
    
    Image* img;
    FILE* f = fopen(path, "rb");
    size_t items_read;

    if(f == NULL) {
        perror("Could not open file");
        return NULL;
    }

    fread(magic_num, sizeof(unsigned char), 2, f);
    
    if(!(magic_num[0] == 'B' && magic_num[1] == 'M')) {
        fprintf(stderr, "Not a valid bitmap file\n");
        fclose(f);
        return NULL;
    }

    fseek(f, 0x0A, SEEK_SET);
    fread(&data_offset, sizeof(int), 1, f);

    fread(&dib_size, sizeof(int), 1, f);
    if(dib_size != 40) {
        fprintf(stderr, "Only V3 bitmap files supported!\n");
        fclose(f);
        return NULL;
    }

    fread(&width, sizeof(int), 1, f);
    fread(&height, sizeof(int), 1, f);
    
    /* Skip color plane count */
    fseek(f, 2, SEEK_CUR);

    fread(&depth, sizeof(short), 1, f);
    if(!(depth == 8 || depth == 24)) {
        fprintf(stderr, "Unsupported bit depth!\n");
        fclose(f);
        return NULL;
    }

    fread(&compression, sizeof(int), 1, f);
    if(compression != 0) {
        fprintf(stderr, "Only uncompresed bitmaps supported\n");
        fclose(f);
        return NULL;
    }

    /* Seek to data segment */
    fseek(f, data_offset, SEEK_SET);

    if(depth == 8) {
        img = Image_new(INDEXED, width, height);
        pixel_size = 1;
    } else {
        img = Image_new(RGB, width, height);
        pixel_size = 3;
    }

    row_size = pixel_size * width;
    data_width = (row_size & 3) ? row_size + (4 - (row_size & 3)) : row_size;
    row_buffer = malloc(data_width);

    for(int row = height - 1; row >= 0; row--) {
        items_read = fread(row_buffer, 1, data_width, f);
        if(items_read != data_width) {
            fprintf(stderr, "err: %d %d %d\n", row, items_read, data_width);
        }
        for(int col = 0; col < width; col++) {
            if(img->mode == INDEXED) {
                /* Indexed */
                img->data.indexed[(row_size * row) + col] = row_buffer[col];
            } else {
                /* RGB */
                img->data.rgb[(width * row) + col].r = row_buffer[(col * pixel_size) + 2];
                img->data.rgb[(width * row) + col].g = row_buffer[(col * pixel_size) + 1];
                img->data.rgb[(width * row) + col].b = row_buffer[(col * pixel_size) + 0];
            }
        }
    }

    fclose(f);
    return img;
}

void Bitmap_write(Image* img, const char* path) {
    /* File to write to */
    FILE* f;

    /* BMP header */
    unsigned char magic_num[2] = "BM";
    unsigned int bmp_size;  /* set below */
    unsigned int reserved = 0;
    unsigned int data_offset = 54;

    /* DIB header */
    unsigned int dib_size = 40;
    unsigned int width = img->width;
    unsigned int height = img->height;
    unsigned short color_planes = 1;
    unsigned short depth;         /* set below */
    unsigned int compression = 0;
    unsigned int data_size;       /* set below */
    unsigned int hres = 11811;    /* Typical */
    unsigned int vres = 11811;
    unsigned int palette_size = 0;
    unsigned int important_colors = 0;

    /* Calculated values */
    unsigned short pixel_size;
    unsigned int row_size;
    unsigned int data_width;

    /* Row buffer */
    unsigned char* row_buffer;
    unsigned int palette_item;

    /* Determine depth */
    if(img->mode == INDEXED) {
        depth = 8;
        palette_size = img->palette_size;
    } else {
        depth = 24;
    }

    /* Determine size */
    pixel_size = depth / 8;
    row_size = width * pixel_size;
    data_width = (row_size & 3) ? row_size + (4 - (row_size & 3)) : row_size;
    data_size = data_width * height;

    /* Data size + header size */
    bmp_size = data_size + 54;

    /* Open file */
    f = fopen(path, "wb");
    if(f == NULL) {
        perror("Unable to open file");
        return;
    }

    /* Write BMP header */
    fwrite(&magic_num, sizeof(char), 2, f);
    fwrite(&bmp_size, sizeof(int), 1, f);
    fwrite(&reserved, sizeof(int), 1, f);
    fwrite(&data_offset, sizeof(int), 1, f);

    /* Write DIB header */
    fwrite(&dib_size, sizeof(int), 1, f);
    fwrite(&width, sizeof(int), 1, f);
    fwrite(&height, sizeof(int), 1, f);
    fwrite(&color_planes, sizeof(short), 1, f);
    fwrite(&depth, sizeof(short), 1, f);
    fwrite(&compression, sizeof(int), 1, f);
    fwrite(&data_size, sizeof(int), 1, f);
    fwrite(&hres, sizeof(int), 1, f);
    fwrite(&vres, sizeof(int), 1, f);
    fwrite(&palette_size, sizeof(int), 1, f);
    fwrite(&important_colors, sizeof(int), 1, f);

    /* Write the indexed palette */
    if(img->mode == INDEXED) {
        for(int i = 0; i < palette_size; i++) {
            palette_item = img->palette[i].b | (img->palette[i].g << 8) | (img->palette[i].r << 16);
            fwrite(&palette_item, sizeof(int), 1, f);
        }
    }

    /* Ready write buffer */
    row_buffer = calloc(sizeof(char), data_width);

    for(int row = height - 1; row >= 0; row--) {
        for(unsigned int col = 0; col < width; col++) {
            if(img->mode == INDEXED) {
                /* Indexed */
                row_buffer[col * pixel_size] = img->data.indexed[(row * width) + col];
            } else {
                /* RGB */
                row_buffer[(col * pixel_size) + 2] = img->data.rgb[(row * width) + col].r;
                row_buffer[(col * pixel_size) + 1] = img->data.rgb[(row * width) + col].g;
                row_buffer[(col * pixel_size) + 0] = img->data.rgb[(row * width) + col].b;
            }
        }
        fwrite(row_buffer, sizeof(char), data_width, f);
    }

    fclose(f);
}
