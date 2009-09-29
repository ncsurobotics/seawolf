/*bitmap.h - part of the vision program
 *
 * Author: Robert Brooks Stephenson
 * Date: 1.30.2009
 *
 */

#define MAX_NUMBER_OF_OBJECTS 1310720


//Bitmap file header - required data for proper loading/saving of bitmaps
typedef struct {
   unsigned short type;
   unsigned long size;
   unsigned short reserved1;
   unsigned short reserved2;
   unsigned long offsetbits;
} BITMAPFILEHEADER;

//Bitmap file header - required data for proper loading/saving of bitmaps.  Similar to file header, but with more details.
typedef struct {
   unsigned long size;
   unsigned long width;
   unsigned long height;
   unsigned short planes;
   unsigned short bitcount;
   unsigned long compression;
   unsigned long sizeimage;
   long xpelspermeter;
   long ypelspermeter;
   unsigned long colorsused;
   unsigned long colorsimportant;
} BITMAPINFOHEADER;

//Struct to hold a single 24-bit RGB color pixel
typedef struct {
   unsigned char blue;
   unsigned char green;
   unsigned char red;
} SINGLE_PIXEL;
 

//Struct to hold all the necessary info for describing a bitmap
//NOTE: YOU MUST ALLOCATE THE BITMAP ARRAY BEFORE USING IT!!!
typedef struct{
	SINGLE_PIXEL** bitmap;
	BITMAPFILEHEADER file_header;
	BITMAPINFOHEADER info_header;
} IMAGE;


//Struct to hold the information that describes a located object
typedef struct {
	unsigned char blue;
	unsigned char green;
	unsigned char red;
	int top;
	int bottom;
	int left;
	int right;
	unsigned int number;
	short active;
} OBJECT;
	

//Function prototypes

//These functions reside in bitmap_io.c
int get_bitmap(char* filename, IMAGE* input_image);
int write_bitmap(char* filename, IMAGE* input_image);
int copy_header(IMAGE* input_image, IMAGE* output_image);
void print_image_header(IMAGE* input_image);

//These fnctions reside in process_image.c
int process_image(IMAGE* input_image, IMAGE* output_image, SINGLE_PIXEL* threshold, int size, SINGLE_PIXEL* deviation, SINGLE_PIXEL* multiplier);
OBJECT* find_objects(IMAGE* input_image, SINGLE_PIXEL* threshold, SINGLE_PIXEL* deviation);
int boxbound(int top, int bottom, int left, int right, IMAGE* input_image, SINGLE_PIXEL bndbox);
void edge_detect(IMAGE* input_image, IMAGE* output_image);
void multiply_image(IMAGE* input_image, SINGLE_PIXEL* multiplier);
void threshold_image(IMAGE* input_image, SINGLE_PIXEL* threshold);
void combine_objects(int obj1, int obj2, OBJECT* objects);
void bw(IMAGE* input_image, IMAGE* output_image, int mode);
unsigned char histogram(IMAGE* input_image);
IMAGE* hough(IMAGE* input_image, SINGLE_PIXEL* threshold);
void box_objects(OBJECT* objects, IMAGE* input_image, int selection);
void hough_lines(OBJECT* objects, IMAGE* input_image, int max_radius);
void fft(IMAGE* input_image);
