
#ifndef __IMAGE_PROCESS_HEADER_
#define __IMAGE_PROCESS_HEADER_

#include <stdbool.h>
#include <opencv/cv.h>

typedef unsigned char IndexedPixel;

struct RGBPixel_s {
    unsigned char r;
    unsigned char g;
    unsigned char b;
};

enum ColorMode {
    RGB,
    INDEXED
};

struct Image_s {
    unsigned int width;
    unsigned int height;
    enum ColorMode mode;
    union {
        struct RGBPixel_s* rgb;
        IndexedPixel* indexed;
    } data;
    struct RGBPixel_s* palette;
    unsigned short palette_size;
};

typedef struct Image_s Image;
typedef struct RGBPixel_s RGBPixel;

#ifndef __IMAGE__
extern RGBPixel WHITE;
extern RGBPixel BLACK;
extern RGBPixel RED;
extern RGBPixel GREEN;
extern RGBPixel BLUE;
extern RGBPixel YELLOW;
extern RGBPixel ORANGE;
#endif

/* Bitmap IO */
Image* Bitmap_read(const char* path);
void Bitmap_write(Image* img, const char* path);

/* Image allocation */
Image* Image_new(enum ColorMode mode, unsigned int width, unsigned int height);
Image* Image_newFrom(Image* img);
Image* Image_duplicate(Image* img);
void Image_destroy(Image* img);
void Image_copy(Image* src, Image* dest);

/* Misc functions */
int* Int_new(int n);
float* Float_new(float n);
float Pixel_diff(RGBPixel* px_1, RGBPixel* px_2);
bool Pixel_equal(RGBPixel* px_1, RGBPixel* px_2);
RGBPixel Pixel_normalize(RGBPixel* px, int brightness);
float Pixel_brightness(RGBPixel* px);

/* Image processing */
void Image_nr(Image* in, Image* out, float sensitivity);
void Image_edgeDetect(Image* in, Image* out, float sensitivity);
void Image_indexedToRGB(Image* in, Image* out);
void Image_toGrayscale(Image* in, Image* out);
void Image_colorFilter(Image* in, Image* out, RGBPixel* color, int count);
void Image_toMonochrome(Image* in, Image* out);
void Image_colorMask(Image* in, Image* out, RGBPixel* color, float stddev);
void Image_reduceRGB(Image* in, Image* out);
void Image_reduceSpectrum(Image* in, Image* out, unsigned short color_count, float stddev);
void Image_identifyBlobs(Image* in, Image* out);
void Image_boxBlob(Image* in, Image* out);
int Image_blobCenter(Image* in);
void Image_removeColor(Image* in, Image* out, RGBPixel* color, int repeat);
void Image_blur(Image* in, Image* out, int rounds);
void Image_normalize(Image* in, Image* out, short brightness);

/* Image <--> IplImage */
void IplImageToImage(IplImage* src, Image* dest);
void ImageToIplImage(Image* src, IplImage* dest);

#endif // #ifndef __IMAGE_PROCESS_HEADER_
