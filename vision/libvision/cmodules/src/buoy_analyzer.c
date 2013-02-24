
#include <stdio.h>
#include <cv.h>
#include <highgui.h>
#include <math.h>
#include <seawolf.h>

/* FILE CONTAINS:           */
/* buoy_color ()          */

#define RED    1
#define GREEN  2
#define YELLOW 3

#define VISUAL_DEBUG

/* PROTOTYPES */
typedef struct BuoyROI_s {
    int x;
    int y;
    int w;
    int h;
} BuoyROI;

struct RGBPixel_s {
    unsigned char r;
    unsigned char g;
    unsigned char b;
};

typedef struct RGBPixel_s RGBPixel;

//color identification
int* buoy_color(IplImage* src, BuoyROI** rois, int num_rois);
RGBPixel* average_region(IplImage* src, BuoyROI* roi); 
double Pixel_dist_rgb(RGBPixel* px_1, RGBPixel* px_2);
void analyze_region(IplImage* src, BuoyROI* roi, double* distances, RGBPixel* avg_color);

/**
 * \brief computes distance between two pixels in rgb space
 * \private
 */
double Pixel_dist_rgb(RGBPixel* px_1, RGBPixel* px_2) {
    int red = px_1->r - px_2->r;
    int green = px_1->g - px_2->g;
    int blue = px_1->b - px_2->b;
    return sqrt(pow((short)red, 2) +
                pow((short)green, 2) +
                pow((short)blue, 2));
}

/* FUNCTION: average_region */
/*                          */
/*  averages color over roi */

RGBPixel* average_region(IplImage* src, BuoyROI* roi){
    /* walk through relevant region of source and compute average color */
    double avg_r = 0;
    double avg_g = 0;
    double avg_b = 0;

    int x, y;
    for(y = roi->y; y < roi->y + roi->h; y++){
        for( x = roi->x; x < roi->x + roi->w; x++){
            avg_r += (unsigned char)src->imageData[y*src->widthStep + 3*x + 2] ;
            avg_g += (unsigned char)src->imageData[y*src->widthStep + 3*x + 1] ;
            avg_b += (unsigned char)src->imageData[y*src->widthStep + 3*x + 0] ;
        }
    }

    avg_r /= (roi->w * roi->h);
    avg_g /= (roi->w * roi->h);
    avg_b /= (roi->w * roi->h);

    RGBPixel* avg_color = malloc(sizeof(RGBPixel));
    avg_color->r = (unsigned char)avg_r;
    avg_color->g = (unsigned char)avg_g;
    avg_color->b = (unsigned char)avg_b;

    return avg_color;
}

/* FUNCTION: analyze_region                 */
/*                                               */
/* determines strongest color of a region        */

void analyze_region(IplImage* src, BuoyROI* roi, double* distances, RGBPixel* avg_color){
    /* walk through relevant region of source and compute average color */
    /*  weighted by deviation from grey */
    double avg_r = 0;
    double avg_g = 0;
    double avg_b = 0;

    int x, y, px;
    double r, g, b, shift;
    int scaled_r, scaled_g, scaled_b;
    double weight;
    uchar* srcData = src->imageData;
    for(y = roi->y; y < roi->y + roi->h; y++){
        for( x = roi->x; x < roi->x + roi->w; x++){
            px = y*src->widthStep + x*3;

            r = (int)srcData[px + 2] - (int)avg_color->r + 127;
            g = (int)srcData[px + 1] - (int)avg_color->g + 127;
            b = (int)srcData[px + 0] - (int)avg_color->b + 127;

            /* determine distance from each color */

            /* determine distance from neutral */
            weight = sqrt(pow(r, 2) + pow(g, 2) + pow(b, 2));
            weight /= 441;

            r = r * weight * weight * 4;
            g = g * weight * weight * 4;
            b = b * weight * weight * 4;

            /* add new r and g vectors */
            avg_r += r * weight;
            avg_g += g * weight;
        }
    }

    /* determine average 2-d vector */
    avg_r /= (roi->w * roi->h);
    avg_g /= (roi->w * roi->h);

    //printf("avg_r = %lf, avg_g = %lf \n",avg_r, avg_g);
    /* determine dot product to use as distance from each color vector of interest */
    /* Grey */
    distances[0] = sqrt(pow(avg_r,2) + pow(avg_g,2));
    /* Red */
    distances[RED] = avg_r / distances[0];
    /* Green */
    distances[GREEN] = avg_g / distances[0];
    /* Yellow */
    distances[YELLOW] = (.707*avg_r + .707*avg_g) / distances[0];
}

/* FUNCTION: buoy_color() */

int* buoy_color(IplImage* src, BuoyROI** rois, int num_rois){

    /* looping indicies */
    int color_idx, rank;
    int x,y,px;

    /* compute average color of horizontal region containing ROI's */
    int min_y = src->height;
    int max_y = 0;
    int roi;

    /* Find rows that bound the regions of interest */
    for ( roi = 0; roi < num_rois; roi++){
        if(rois[roi]->y < min_y)
            min_y = rois[roi]->y;
        if(rois[roi]->y + rois[roi]->h > max_y)
            max_y = rois[roi]->y + rois[roi]->h;
    }

    /* Pack bounding rows into a ROI structure */
    BuoyROI total_vert_roi;
    total_vert_roi.x = 0;
    total_vert_roi.w = src->width;
    total_vert_roi.y = min_y;
    total_vert_roi.h = max_y - min_y;

    /* determine average color of bounding region */
    RGBPixel* avg_color = average_region(src, &total_vert_roi);

    /* determine and sort by average color of each roi */
    RGBPixel** avg_roi_colors = malloc(num_rois*sizeof(RGBPixel*)); //list of average colors
    double** distances = malloc(num_rois * sizeof(double*)); // list of distances from each color
    for(roi = 0; roi < num_rois; roi ++){
        avg_roi_colors[roi] = malloc(sizeof(RGBPixel));
        distances[roi] = malloc(4*sizeof(double));
    }

    /* two dimensional array to sort the proximity of buoys to each color */
    int** best_roi = malloc(3*sizeof(int*)); //list of best ROI's for each color
    for( color_idx = 0; color_idx < 3; color_idx++){
        best_roi[color_idx] = calloc(num_rois+1, sizeof(int));
        best_roi[color_idx][num_rois] = -1;
    }


    for ( roi = 0; roi < num_rois; roi++){

        /* determine 'distance's from each color */
        analyze_region(src, rois[roi], distances[roi], avg_color);

#if 0
        avg_roi_colors[roi] = average_region(src, rois[roi]);

        /* normalize roi color */
        int scaled_r = avg_roi_colors[roi]->r + 127 - (int)avg_color->r;
        int scaled_g = avg_roi_colors[roi]->g + 127 - (int)avg_color->g;
        int scaled_b = avg_roi_colors[roi]->b + 127 - (int)avg_color->b;

        /* keep adjusted values between 0 and 255 */
        avg_roi_colors[roi]->r = Util_inRange(0, scaled_r, 255);
        avg_roi_colors[roi]->g = Util_inRange(0, scaled_g, 255);
        avg_roi_colors[roi]->b = Util_inRange(0, scaled_b, 255);

        /* determine distance from image average */
        RGBPixel grey = {127, 127, 127};
        distances[roi][0] = Pixel_dist_rgb(&grey, avg_roi_colors[roi]);

        /* determine distance from red */
        RGBPixel red = {255,0,0};
        distances[roi][RED] = Pixel_dist_rgb(&red, avg_roi_colors[roi]);

        /* determine distance from green */
        RGBPixel green = {0,255,0};
        distances[roi][GREEN] = Pixel_dist_rgb(&green, avg_roi_colors[roi]);

        /* determine distance from yellow */
        RGBPixel yellow = {255,255,0};
        distances[roi][YELLOW] = Pixel_dist_rgb(&yellow, avg_roi_colors[roi]);
        distances[roi][YELLOW] /= 1.41; //normalize because geometry

#endif
        /* sort this roi into the list of distances by color*/
        if ( roi == 0 ) continue;

        int sorted_roi, new_roi;
        for( color_idx = 0; color_idx < 3; color_idx ++) {
            new_roi = roi;
            for ( rank = 0; rank < roi; rank++) {
                sorted_roi = best_roi[color_idx][rank];
                if ( distances[new_roi][color_idx+1] > distances[sorted_roi][color_idx+1] ) {
                    /* place cur_roi here, and pick up sorted_roi */
                    best_roi[color_idx][rank] = new_roi;
                    new_roi = sorted_roi;
                }
            }
            /*place the roi we are currently handling into last place */
            best_roi[color_idx][roi] = new_roi;
        }
    }
#if 0
    printf("printing best_roi matrix: \n");
    for(color_idx = 0; color_idx < 3; color_idx++){
        printf("color %d: ",color_idx);
        for(rank = 0; rank <= num_rois; rank++){
            printf(" %d ; ",best_roi[color_idx][rank]);
        }
        printf("\n");
    }
#endif

    /* now make sure that no roi is considered two diferent colors */
    int i,j;
    for( i = 0; i < 2; i++ ){
        for ( j = i + 1; j < 3; j++) {
            if (best_roi[i][0] == best_roi[j][0] && best_roi[i][0] >= 0){
                /* one buoy is considerd two colors. determine which suits it best */
                int duplicate = best_roi[i][0];
                int worse_color;
                if ( distances[duplicate][i] < distances[duplicate][j])
                    worse_color = j;
                else
                    worse_color = i;

                /* delete this roi from the buoy rankings it was worse at */
                for ( rank = 0; rank < num_rois; rank++)
                    best_roi[worse_color][rank] = best_roi[worse_color][rank+1];

                /* restart the algorithm */
                i = 0;
                j = i + 1;
            }
        }
    }
#if 0
    printf("printing best_roi matrix: \n");
    for(color_idx = 0; color_idx < 3; color_idx++){
        printf("color %d: ",color_idx);
        for(rank = 0; rank <= num_rois; rank++){
            printf(" %d ; ",best_roi[color_idx][rank]);
        }
        printf("\n");
    }
    printf ("------------------------------\n");
#endif

    /* initialize the array that will hold final color data for each buoy */
    int* color_sequence;
    color_sequence = (int*)calloc(num_rois, sizeof(int));

    /* populate color_sequence */
    for ( roi = 0; roi < num_rois; roi++){
        for (color_idx = 0; color_idx < 3; color_idx++ ){
            if ( roi == *best_roi[color_idx] ){
                color_sequence[roi] = color_idx+1;
                break;
            }
        }
    }

    #ifdef VISUAL_DEBUG
        /* create and display a normalized version of src */
        IplImage* debug = cvCloneImage(src);

        double r, g, b;
        int min, max;
        int scaled_r, scaled_g, scaled_b;
        double weight,shift, px_x, px_y;
        uchar* debugData = (uchar*) debug->imageData;
        for(x=src->width-1; x>=0;x--){
            for(y=src->height-1; y>=0;y--){

                px = y*src->widthStep + x*3;

                r = (int)debugData[px + 2] - (int)avg_color->r;
                g = (int)debugData[px + 1] - (int)avg_color->g;
                b = (int)debugData[px + 0] - (int)avg_color->b;

                /* remove intensity */
                shift = (r + g + b)/1.73;
                r = r - shift;
                g = g - shift;
                b = b - shift;

                /* determine distance from neutral */
                weight = sqrt(pow(r, 2) + pow(g, 2) + pow(b, 2));
                weight /= 441;

                r = r * weight * weight * 4;
                g = g * weight * weight * 4;
                b = b * weight * weight * 4;

                r += 127;
                g += 127;
                b += 127;

                /* keep adjusted values between 0 and 255 */
                debugData[px + 2] = Util_inRange(0, r, 255);
                debugData[px + 1] = Util_inRange(0, g, 255);
                debugData[px + 0] = Util_inRange(0, b, 255);
            }
        }

        CvPoint tl = {total_vert_roi.x,total_vert_roi.y};
        CvPoint br = {tl.x + total_vert_roi.w, tl.y + total_vert_roi.h};
        CvScalar color =  {avg_color->b, avg_color->g, avg_color->r, 0};
        cvRectangle(debug, tl, br,color, 5, 8, 0);
        //cvNamedWindow("Color Analyzer Debug", CV_WINDOW_AUTOSIZE);
        //cvShowImage("Color Analyzer Debug", debug);

        cvReleaseImage(&debug);
    #endif

    /* free resources */
    free(avg_color);
    for( roi = 0; roi < num_rois; roi++){
        free(avg_roi_colors[roi]);
        free(distances[roi]);
    }
    free(avg_roi_colors);
    free(distances);
    for( color_idx = 0; color_idx < 3; color_idx++)
        free(best_roi[color_idx]);
    free(best_roi);

    return color_sequence;
}
