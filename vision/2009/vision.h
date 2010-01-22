#ifndef __SEAWOLF3_VISION
#define __SEAWOLF3_VISION

#include <stdbool.h>
#include <highgui.h>
#include <opencv/cv.h>

#define WAIT 0
//EACH REAL MISSION INCLUDES FINDING THE NEXT APPROPRIATE MARKER (SINCE THAT IS SPECIFIC TO EACH MISSION) THEN ALLIGN_PATH ALLIGNS US WITH THAT MARKER
#define GATE 1 
#define GATE_PATH 11
#define BOUEY 3
#define BOUEY_PATH 33
#define BARBED_WIRE 4
#define BARBED_WIRE_ALLIGN 42
#define BARBED_WIRE_PATH 44
#define TORPEDO 5
#define TORPEDO_PATH 55
#define BOMBING_RUN 6
#define BOMBING_RUN_PATH 66
#define BOMBING_RUN_2 61
#define BOMBING_RUN_2_PATH 661
#define BRIEFCASE 7
#define BRIEFCASE_GRAB 77
#define OCTOGON 8
#define ALLIGN_PATH 9 //CALLED AFTER FINDING THE CORRECT PATH AFTER EACH MISSION, ONCE COMPLETED, RETURN RETURN TASK COMPLETE
#define IDENTIFY_SILHOUET 10
#define TUNA_BLOB 12
#define MOTION 13

typedef struct {
    CvPoint pt[4]; //holds the four corners
    CvPoint mid;   //holds the middle of the region (populated in mission.c
    double avgr; //average color of the region
    double avgg;
    double avgb;
    int area;//area of the region
    int type; //0=not a bin 1=battleship 2=airplane 3=factory 4= tank 5=don't know, but it's a bin
} REGION;
typedef struct{
    int rows; //holds number of rows of the grid
    int columns; //holds  number of columns in grid
    REGION** region; //holds the regions of the grid
} GRID;

typedef struct{ 
	int top;
	int left;
	int right;
	int bottom; 
	long int area;
	double cent_x;
	double cent_y;
	CvPoint mid;
	CvPoint* pixels; 
} BLOB;

// hough_opencv.c
void hough_opencv_init();
CvSeq* hough_opencv(IplImage* img, IplImage* original, int threshold, int linesMax,int targetAngle, int angleThreshold, int clusterSize, int clusterWidth, int clusterHeight);
void hough_opencv_free();

// grid.c
void grid_init();
void find_regions(CvSeq* lines, GRID* grid, IplImage* frame);
void find_bins(GRID* grid, IplImage* frame);
void combine_bins(GRID* grid, IplImage* frame);
void determine_type(GRID* grid, IplImage* frame);
int analyze_bin(IplImage* isolated, int binArea);
void grid_free();

// motion.c
void blob_motion(IplImage* frame);
void blob_motion_init();
void blob_motion_free();

// edge_opencv.c
void edge_opencv_init();
IplImage* edge_opencv(IplImage* frame, int low_threshold, int high_threshold, int aperture);
void edge_opencv_free();

// colorfilter.c
void colorfilter_init();
IplImage* colorfilter(IplImage* img, int rmin, int rmax, int bmin, int bmax, int gmin, int gmax);
void colorfilter_free();

// blob.c
void blob_init();
int blob(IplImage* Img, BLOB** blobs, int tracking_number, int minimum_blob_area);
BLOB* findPrimary(IplImage* Img, int target_number, int minimum_blob_area, int *blobs_found);
int checkPixel(IplImage* Img, int x, int y, unsigned int** pixlog, BLOB* blob, int depth); 
void blob_copy(BLOB* dest, BLOB* src);
//void blob_free(BLOB* blob, int blobs_found);
void blob_free();

// remove_edges.c
void remove_edges_init();
IplImage* remove_edges(IplImage* img, IplImage* edge, int rmin, int rmax, int bmin, int bmax, int gmin, int gmax);
void remove_edges_free();

// camera.c
int frame_number;
CvCapture* init_camera_from_args(int argc, char** argv);
CvCapture* init_camera_from_string(char* str);
void multicam_set_camera(int camnumber, char* camstr);
void multicam_reset_camera();
IplImage* multicam_get_frame(int camnumber);
IplImage* get_frame(CvCapture* capture);
#define DOWN_CAM 0
#define FORWARD_CAM 1
#define UP_CAM 2



//******************************************************************************************
// Tunavision header
//******************************************************************************************

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
void tuna_init();
int* Int_new(int n);
float* Float_new(float n);
float Pixel_stddev(RGBPixel* px_1, RGBPixel* px_2);
bool Pixel_equal(RGBPixel* px_1, RGBPixel* px_2);
RGBPixel Pixel_normalize(RGBPixel* px, int brightness);
float Pixel_brightness(RGBPixel* px);

/* Image processing */
void Image_indexedToRGB(Image* in, Image* out);
void Image_toGrayscale(Image* in, Image* out);
void Image_colorFilter(Image* in, Image* out, RGBPixel* color, int count);
void Image_toMonochrome(Image* in, Image* out);
void Image_colorMask(Image* in, Image* out, RGBPixel* color, float stddev);
void Image_reduceRGB(Image* in, Image* out);
int Image_reduceSpectrum(Image* in, Image* out, unsigned short color_count, int* stddev);
void Image_identifyBlobs(Image* in, Image* out);
void Image_boxBlob(Image* in, Image* out);
int Image_blobCenter(Image* in);
void Image_removeColor(Image* in, Image* out, RGBPixel* color, int repeat);
void Image_blur(Image* in, Image* out, int rounds);
void Image_normalize(Image* in, Image* out);
int FindTargetColor(Image* in, Image* out, RGBPixel* color, int min_blobsize, int dev_threshold);

/* mission_state.c */
void wait_for_go();
int mission_done();

/* Image <--> IplImage */
void IplImageToImage(IplImage* src, Image* dest);
void ImageToIplImage(Image* src, IplImage* dest);

#endif // #ifndef __IMAGE_PROCESS_HEADER_
