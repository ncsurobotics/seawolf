#ifndef __SEAWOLF_VISION_LIB_GRID_INCLUDE_H
#define __SEAWOLF_VISION_LIB_GRID_INCLUDE_H

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

void grid_init(void);
void find_regions(CvSeq* lines, GRID* grid, IplImage* frame);
void find_bins(GRID* grid, IplImage* frame);
void combine_bins(GRID* grid, IplImage* frame);
void determine_type(GRID* grid, IplImage* frame);
int analyze_bin(IplImage* isolated, int binArea);
void grid_free(void);

#endif
