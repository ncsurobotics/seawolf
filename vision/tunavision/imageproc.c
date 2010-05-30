
#include "seawolf.h"
#include "img.h"

/* indexed -> rgb */
void Image_indexedToRGB(Image* in, Image* out) {
    int width = in->width;
    int height = in->height;
    IndexedPixel* in_data = in->data.indexed;
    RGBPixel* out_data = out->data.rgb;

    for(int i = width * height - 1; i >= 0; i--) {
        out_data[i] = in->palette[in_data[i]];
    }
}

/* rgb -> indexed */
void Image_toGrayscale(Image* in, Image* out) {
    int width = in->width;
    int height = in->height;
    RGBPixel* in_data = in->data.rgb;
    IndexedPixel* out_data = out->data.indexed;

    out->palette_size = 256;
    for(int i = 0; i < 256; i++) {
        out->palette[i].r = i;
        out->palette[i].g = i;
        out->palette[i].b = i;
    }
    
    for(int i = width * height - 1; i >= 0; i--) {
        out_data[i] = Pixel_brightness(&in_data[i]);
    }
}

/* indexed -> indexed */
void Image_colorFilter(Image* in, Image* out, RGBPixel* color, int count) {
    int low_items[count];
    int current_highdev;
    float highdev;
    float thisdev;
    
    RGBPixel average_color;
    int r = 0, 
        g = 0, 
        b = 0;
    
    for(int i = 0; i < count; i++) {
        low_items[i] = i;
    }

    for(int i = 1; i < in->palette_size; i++) {
        current_highdev = 0;
        for(int j = 1; j < count; j++) {
            thisdev = Pixel_diff(color, &in->palette[low_items[j]]);
            highdev = Pixel_diff(color, &in->palette[low_items[current_highdev]]);
            if(thisdev > highdev) {
                current_highdev = j;
            }
        }

        highdev = Pixel_diff(color, &in->palette[low_items[current_highdev]]);
        thisdev = Pixel_diff(color, &in->palette[i]);
        if(thisdev < highdev) {
            low_items[current_highdev] = i;
        }
    }

    for(int i = 0; i < count; i++) {
        r += in->palette[low_items[i]].r;
        g += in->palette[low_items[i]].g;
        b += in->palette[low_items[i]].b;
    }
    
    average_color.r = r / count;
    average_color.g = g / count;
    average_color.b = b / count;

    for(int i = 0; i < count; i++) {
        out->palette[low_items[i]] = average_color;
    }

    for(int i = 0; i < in->palette_size; i++) {
        if(! Pixel_equal(&average_color, &out->palette[i])) {
            out->palette[i] = BLACK;
        }
    }
}

/* indexed -> indexed  */
void Image_toMonochrome(Image* in, Image* out) {
    int width = in->width;
    int height = in->height;
    IndexedPixel* in_data = in->data.indexed;
    IndexedPixel* out_data = out->data.indexed;

    for(int i = width * height - 1; i >= 0; i--) {
        if(Pixel_equal(&in->palette[in_data[i]], &BLACK)) {
            out_data[i] = 0;
        } else {
            out_data[i] = 1;
        }
    }
 
    out->palette_size = 2;
    out->palette[0] = BLACK;
    out->palette[1] = WHITE;
}

/* rgb -> indexed(monochrome)  */
void Image_colorMask(Image* in, Image* out, RGBPixel* color, float stddev) {
    int width = in->width;
    int height = in->height;
    RGBPixel* in_data = in->data.rgb;
    IndexedPixel* out_data = out->data.indexed;

    /* Build binary palette */
    out->palette_size = 2;
    out->palette[0].r = 0;
    out->palette[0].g = 0;
    out->palette[0].b = 0;
    out->palette[1].r = 255;
    out->palette[1].g = 255;
    out->palette[1].b = 255;

    /* Trace image */
    for(int i = width * height - 1; i >= 0; i--) {
        if(Pixel_diff(&in_data[i], color) < stddev) {
            out_data[i] = 1;
        } else {
            out_data[i] = 0;
        }
    }
}

/* rgb -> indexed */
void Image_reduceRGB(Image* in, Image* out) {
    int width = in->width;
    int height = in->height;
    RGBPixel* in_data = in->data.rgb;
    IndexedPixel* out_data = in->data.indexed;
    
    /* Configure palette */
    out->palette_size = 3;
    out->palette[0].r = 255;
    out->palette[0].g = 0;
    out->palette[0].b = 0;
    out->palette[1].r = 0;
    out->palette[1].g = 255;
    out->palette[1].b = 0;
    out->palette[2].r = 0;
    out->palette[2].g = 0;
    out->palette[2].b = 255;

    for(int i = width * height - 1; i >= 0; i--) {
        if(in_data[i].r > in_data[i].g && in_data[i].r > in_data[i].b) {
            out_data[i] = 0;
        } else if(in_data[i].g > in_data[i].r && in_data[i].g > in_data[i].b) {
            out_data[i] = 1;
        } else {
            out_data[i] = 2;
        }
    }
}

/* rgb -> rgb */
void Image_edgeDetect(Image* in, Image* out, float sensitivity) {
    Image* src = Image_duplicate(in);
    int width = in->width;
    int height = in->height;
    RGBPixel* in_data = src->data.rgb;
    RGBPixel* out_data = out->data.rgb;

    int i, r, c, m, n;
    float ar, ag, ab;
    float stddev;
    RGBPixel average;

    const int s = 3;
    const int s_n = s * s;
    const int s_i = -((s-1) / 2);
    const int s_f =  ((s-1) / 2);
    
    for(r = s_f; r < height - s_f; r++) {
        for(c = s_f; c < width - s_f; c++) {
            i = r * width + c;

            stddev = ar = ag = ab = 0.0;
            for(m = s_i; m <= s_f; m++) {
                for(n = s_i; n <= s_f; n++) {
                    ar += in_data[i + (m * width + n)].r;
                    ag += in_data[i + (m * width + n)].g;
                    ab += in_data[i + (m * width + n)].b;
                }
            }

            average.r = (int) ar / s_n;
            average.g = (int) ag / s_n;
            average.b = (int) ab / s_n;

            for(m = s_i; m <= s_f; m++) {
                for(n = s_i; n <= s_f; n++) {
                    stddev += pow(Pixel_diff(&in_data[i + (m * width + n)], &average), 2);
                }
            }
            stddev = sqrt(stddev / s_n);

            if(stddev > sensitivity) {
                out_data[i] = in_data[i];
            } else {
                out_data[i].r = 255;
                out_data[i].g = 255;
                out_data[i].b = 255;
            }
        }
    }
    
    Image_destroy(src);
}

/* rgb -> indexed */
void Image_reduceSpectrum(Image* in, Image* out, unsigned short color_count, float stddev) {
    int width = in->width;
    int height = in->height;
    RGBPixel* in_data = in->data.rgb;
    IndexedPixel* out_data = out->data.indexed;

    RGBPixel temp_pixel;
    double temp_palette[color_count][3];
    unsigned int palette_members[color_count];
    bool match;

    /* Reset palette members */
    for(int i = 0; i < color_count; i++) {
        palette_members[i] = 0;
    }

    /* Configure palette */
    out->palette_size = 0;
    for(int i = 0; i < color_count + 1; i++) {
        out->palette[i].r = 255;
        out->palette[i].g = 255;
        out->palette[i].b = 255;
    }
    
    for(int i = height * width - 1; i >=0; i--) {
        match = false;
        int low_stddev = 256;
        int low_p = 0;
        int tmp_stddev;
        for(int p = 0; p < out->palette_size; p++) {
            temp_pixel.r = (unsigned char) temp_palette[p][0];
            temp_pixel.g = (unsigned char) temp_palette[p][1];
            temp_pixel.b = (unsigned char) temp_palette[p][2];
            tmp_stddev = Pixel_diff(&temp_pixel, &in_data[i]);
            if(tmp_stddev < low_stddev) {
                if(tmp_stddev < stddev) {
                    match = true;
                }
                low_stddev = tmp_stddev;
                low_p = p;
            }
        }

        if(!match && out->palette_size < color_count) {
            /* Create a out palette item */
            temp_palette[out->palette_size][0] = in_data[i].r;
            temp_palette[out->palette_size][1] = in_data[i].g;
            temp_palette[out->palette_size][2] = in_data[i].b;
            palette_members[out->palette_size] = 1;
            out_data[i] = out->palette_size++;
        } else {
            out_data[i] = low_p;
            temp_palette[low_p][0] = ((temp_palette[low_p][0] * palette_members[low_p]) + in_data[i].r) / (palette_members[low_p] + 1);
            temp_palette[low_p][1] = ((temp_palette[low_p][1] * palette_members[low_p]) + in_data[i].g) / (palette_members[low_p] + 1);
            temp_palette[low_p][2] = ((temp_palette[low_p][2] * palette_members[low_p]) + in_data[i].b) / (palette_members[low_p] + 1);
            palette_members[low_p]++;
        }
    }

    for(int i = 0; i < out->palette_size; i++ ) {
        out->palette[i].r = (unsigned char) temp_palette[i][0];
        out->palette[i].g = (unsigned char) temp_palette[i][1];
        out->palette[i].b = (unsigned char) temp_palette[i][2];
    }

    out->palette_size = color_count + 1;
}

struct BlobState_s {
    int i;
    unsigned char p;
};

struct BlobState_s* BlobState_out(int i) {
    struct BlobState_s* bs = malloc(sizeof(struct BlobState_s));
    bs->i = i;
    bs->p = 0;
    return bs;
}

/* indexed(monochrome) -> indexed(monochrome) */
void Image_identifyBlobs(Image* in, Image* _out) {
    int width = in->width;
    int height = in->height;
    Image* out = Image_newFrom(in);
    IndexedPixel* in_data = in->data.indexed;
    IndexedPixel* out_data = out->data.indexed;

    /* Blob data */
    const short bl = 16;
    unsigned int blob_count = 0;
    unsigned int* blob_size = malloc(sizeof(int) * bl);
    int* blob_mask = malloc(sizeof(int) * height * width);
    struct BlobState_s* cur;
    int big_blob = 0;

    /* Pixel trace stack */
    Stack* ptstack = Stack_new();

    /* Offset mapping */
    int offset_map[] = { -width - 1, -width, -width + 1,
                                 -1,                  1,
                          width - 1,  width,  width + 1 };

    /* Initialize blob mask */
    for(int i = height * width - 1; i >= 0; i--) {
        blob_mask[i] = -1;
    }

    for(int i = width * height - 1; i >= 0; i--) {
        if(in_data[i] == 1 && blob_mask[i] == -1) {
            blob_size[blob_count] = 1;
            Stack_push(ptstack, BlobState_out(i));
            while(Stack_getSize(ptstack)) {
                cur = Stack_top(ptstack);
                if(cur->p == 8) {
                    blob_size[blob_count]++;
                    free(Stack_pop(ptstack));
                    continue;
                } else if(cur->p == 0) {
                    blob_mask[cur->i] = blob_count;
                }

                if(in_data[cur->i + offset_map[cur->p]] == 1 && blob_mask[cur->i + offset_map[cur->p]] == -1) {
                    /* Unvisited element */
                    if((cur->i % width == 0 && (cur->p == 1 || cur->p == 2 || cur->p == 4 || cur->p == 6 || cur->p == 7)) || 
                       ((cur->i + 1) % width == 0 && (cur->p == 1 || cur->p == 0 || cur->p == 3 || cur->p == 6 || cur->p == 5)) ||
                       (cur->i % width != 0 && (cur->i + 1) % width != 0)) {
                        Stack_push(ptstack, BlobState_out(cur->i + offset_map[cur->p]));
                    }
                }
                cur->p++;
            }

            /* Is this blob big? */
            if(blob_size[big_blob] < blob_size[blob_count]) {
                big_blob = blob_count;
            }

            /* Bump up blob count */
            blob_count++;

            /* Make more room as necessary */
            if(blob_count % bl == 0) {
                blob_size = realloc(blob_size, sizeof(int) * (blob_count + bl));
            }
        }
    }

    /* Write big blob out to image */
    for(int i = height * width - 1; i >= 0; i--) {
        if(blob_mask[i] == big_blob) {
            out_data[i] = 1;
        } else {
            out_data[i] = 0;
        }
    }

    /* Initialize output palette */
    out->palette_size = 2;
    out->palette[0] = BLACK;
    out->palette[1] = RED;

    Image_copy(out, _out);
    Image_destroy(out);
}

/* indexed(monochrome) -> indexed(monochrome) */
void Image_boxBlob(Image* in, Image* out) {
    int width = in->width;
    int height = in->height;
    IndexedPixel* in_data = in->data.indexed;
    IndexedPixel* out_data = out->data.indexed;

    Image_copy(in, out);

    out->palette_size = 3;
    out->palette[2] = WHITE;

    int top = height;
    int bottom = 0;
    int min_left = width;
    int max_right = 0;

    for(int r = 0; r < height; r++) {
        for(int c = 0; c < width; c++) {
            if(in_data[r * width + c]) {
                if(r < top) {
                    top = r;
                }
                if(r > bottom) {
                    bottom = r;
                }
                if(c < min_left) {
                    min_left = c;
                }
                if(c > max_right) {
                    max_right = c;
                }
            }
        }
    }

    for(int c = min_left; c < max_right; c++) {
        out_data[top * width + c] = 2;
        out_data[bottom * width + c] = 2;
    }
    for(int r = top; r < bottom; r++) {
        out_data[r * width + min_left] = 2;
        out_data[r * width + max_right] = 2;
    }
}

/* indexed(monochrome) -> int */
int Image_blobCenter(Image* in) {
    int width = in->width;
    int height = in->height;
    IndexedPixel* in_data = in->data.indexed;

    int top = height;
    int bottom = 0;
    int min_left = width;
    int max_right = 0;

    for(int r = 0; r < height; r++) {
        for(int c = 0; c < width; c++) {
            if(in_data[r * width + c]) {
                if(r < top) {
                    top = r;
                }
                if(r > bottom) {
                    bottom = r;
                }
                if(c < min_left) {
                    min_left = c;
                }
                if(c > max_right) {
                    max_right = c;
                }
            }
        }
    }

    return (width * ((top + bottom) / 2)) + ((min_left + max_right) / 2);
}

/* indexed -> indexed */
void Image_removeColor(Image* in, Image* out, RGBPixel* color, int repeat) {
    Image_copy(in, out);
    float min_stddev;
    float tmp_stddev;
    int min;

    while(repeat--) {
        for(min = 0; Pixel_equal(&out->palette[min], &BLACK); min++);
        min_stddev = Pixel_diff(color, &out->palette[min]);

        for(int i = min + 1; i < out->palette_size; i++) {
            if(Pixel_equal(&out->palette[i], &BLACK)) {
                continue;
            }

            tmp_stddev = Pixel_diff(color, &out->palette[i]);
            if(tmp_stddev < min_stddev) {
                min_stddev = tmp_stddev;
                min = i;
            }
        }
        out->palette[min] = BLACK;
    }
}

void Image_nr(Image* in, Image* out, float sensitivity) {
    Image* src = Image_duplicate(in);
    int width = in->width;
    int height = in->height;
    RGBPixel* in_data = src->data.rgb;
    RGBPixel* out_data = out->data.rgb;

    int i, r, c, m, n;
    float ar, ag, ab;
    float stddev;
    RGBPixel average;

    const int s = 5;
    const int s_n = s * s;
    const int s_i = -((s-1) / 2);
    const int s_f =  ((s-1) / 2);
    
    for(r = s_f; r < height - s_f; r++) {
        for(c = s_f; c < width - s_f; c++) {
            i = r * width + c;

            stddev = ar = ag = ab = 0.0;
            for(m = s_i; m <= s_f; m++) {
                for(n = s_i; n <= s_f; n++) {
                    if(m || n) {
                        ar += in_data[i + (m * width + n)].r;
                        ag += in_data[i + (m * width + n)].g;
                        ab += in_data[i + (m * width + n)].b;
                    }
                }
            }

            average.r = (int) ar / (s_n - 1);
            average.g = (int) ag / (s_n - 1);
            average.b = (int) ab / (s_n - 1);

            for(m = s_i; m <= s_f; m++) {
                for(n = s_i; n <= s_f; n++) {
                    if(m || n) {
                        stddev += pow(Pixel_diff(&in_data[i + (m * width + n)], &average), 2);
                    }
                }
            }
            stddev = sqrt(stddev / (s_n - 1));

            if(Pixel_diff(&in_data[i], &average) < sensitivity) {
                out_data[i] = in_data[i];
            } else {
                out_data[i] = average;
            }
        }
    }
    
    Image_destroy(src);
}

/* rgb -> rgb */
void Image_blur(Image* in, Image* out, int rounds) {
    Image* src = Image_duplicate(in);
    Image* dup = Image_duplicate(in);

    int width = in->width;
    int height = in->height;
    RGBPixel* src_data = src->data.rgb;
    RGBPixel* dup_data = dup->data.rgb;

    int r, g, b;
    int offset_map[] = { -width - 1, -width, -width + 1,
                                 -1,                  1,
                          width - 1,  width,  width + 1 };
    int i;

    while(rounds--) {
        for(int row = 1; row < (height - 1); row++) {
            for(int col = 1; col < (width - 1); col++) {
                i = (row * width) + col;
                r = 0;
                g = 0;
                b = 0;
                for(int j = 0; j < 8; j++) {
                    r += src_data[i + offset_map[j]].r;
                    g += src_data[i + offset_map[j]].g;
                    b += src_data[i + offset_map[j]].b;
                }
                dup_data[row * width + col].r = r / 8;
                dup_data[row * width + col].g = g / 8;
                dup_data[row * width + col].b = b / 8;
            }
        }
        Image_copy(dup, src);
    }

    Image_copy(dup, out);
    Image_destroy(src);
    Image_destroy(dup);
}

/* rgb -> rgb */
void Image_normalize(Image* in, Image* out, short brightness) {
    int width = in->width;
    int height = in->height;
    RGBPixel* in_data = in->data.rgb;
    RGBPixel* out_data = out->data.rgb;
    
    for(int i = width * height - 1; i >= 0; i--) {
        out_data[i] = Pixel_normalize(&in_data[i], brightness);
    }
}
