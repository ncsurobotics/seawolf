#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>

#include "vision_lib.h"
#include <cv.h>
#include <highgui.h>

// This file contains code to parse out reginos from houglines
void grid_init(){
  #ifdef debug_grid
    cvNamedWindow("Grid", CV_WINDOW_AUTOSIZE);
  #endif
  #ifdef debug_bins
    cvNamedWindow("Bin1",CV_WINDOW_AUTOSIZE);
    cvNamedWindow("Bin2",CV_WINDOW_AUTOSIZE);
    cvNamedWindow("Bin3",CV_WINDOW_AUTOSIZE);
    cvNamedWindow("Bin4",CV_WINDOW_AUTOSIZE);
  #endif
}

void find_regions(CvSeq* lines, GRID* grid, IplImage* frame) {
            #define NUMLINES 20
            int i,j,k,l;
            float* line = (float*)cvGetSeqElem(lines,NUMLINES-1);
            double ang1 = line[1];
	    double ang2 = 0;
            int rho1[NUMLINES];
            int rho2[NUMLINES];
            int rhocount1 = 0;
            int rhocount2 = 0;
            CvPoint intersects[NUMLINES*NUMLINES];
            int intersectcount = 0;

            //Sort the lines by their angle
            //Lines with an angle like the most dominant line go in rho1
            //Others go in rho2
            for(i=0;i<NUMLINES;i++)
            {
		float pi = 3.14159;//FOR SOME REASON 'PI' ISN'T WORKING
                line = (float*)cvGetSeqElem(lines,i);
                if (line[0] == -999) continue;
                double ang = line[1];
                double offset = fabs(ang1-ang);
                if (offset < 0.15 || fabs(offset-pi) < 0.15){
                    rho1[rhocount1++] = i;
                }else if(fabs(offset-pi/2) < 0.15 || fabs(offset-3*pi/2) < 0.15) {
		    ang2 = ang;
                    rho2[rhocount2++] = i;
                }
            }
            //Sort lines in rho1 by their y value if horizonatal, x value if vertical
            double rho1tmp[NUMLINES];
            int rho1tmpcount = 0;
            for (i=0;i<rhocount1;i++)
            {
                line = (float*)cvGetSeqElem(lines,rho1[i]);
                float rho = line[0];
                float theta = line[1];
                double a = cos(theta), b = sin(theta);
                double x0 = a*rho, y0 = b*rho;
                double pt1x,pt1y,pt2x,pt2y;
                pt1x = x0 + 1000*(-b);
                pt1y = y0 + 1000*(a);
                pt2x = x0 - 1000*(-b);
                pt2y = y0 - 1000*(a);
                double M,B;
                if (fabs(pt1x-pt2x) > fabs(pt1y-pt2y) )
                {   //the line is roughly horizontal
                    M = (pt1y-pt2y)/(pt1x-pt2x);
                    B = M*(0-pt2x)+pt2y;
                    //cvCircle(frame,cvPoint(0,B),5,cvScalar(0,255,0,0),1,8,0);
	            //printf("rho1 line[%d] M = %f B = %f is horizontal\n",i,M,B);
                    rho1tmp[rho1tmpcount++] = B;
                } else if( (int)(pt1x-pt2x) == 0) {
		    //the line is exactly vertical
                    //cvCircle(frame,cvPoint(pt1x,0),5,cvScalar(0,255,0,0),1,8,0);
	            //printf("rho1 line[%d] is exactly vertical\n",i);
                    rho1tmp[rho1tmpcount++] = pt1x;		    
		} else{
		    //the line is roughly vertical
                    M = (pt1y-pt2y)/(pt1x-pt2x);
                    B = M*(0-pt2x)+pt2y;
                    //cvCircle(frame,cvPoint(-B/M,0),5,cvScalar(0,255,0,0),1,8,0);
	            //printf("rho1 line[%d] M = %f B = %f -B/M = %f is vertical \n",i,M,B,-B/M);
		    rho1tmp[rho1tmpcount++] = -B/M;
                }
            }
            int issorted = 0;
            while (!issorted)
            {
                    issorted=1;
	            for(i=0;i<rhocount1-1;i++)
	            {
	                if (rho1tmp[i] < rho1tmp[i+1])
	                {
                            issorted=0;
	                    double tmp = rho1tmp[i];
	                    rho1tmp[i] = rho1tmp[i+1];
	                    rho1tmp[i+1] = tmp;
			    int tmprho = rho1[i];
			    rho1[i] = rho1[i+1];
			    rho1[i+1] = tmprho;
	                }
	            }
             }
            //Sort lines in rho2 by their y value if horizonatal, x value if vertical
            double rho2tmp[NUMLINES];
            int rho2tmpcount = 0;
            for (i=0;i<rhocount2;i++)
            {
                line = (float*)cvGetSeqElem(lines,rho2[i]);
                float rho = line[0];
                float theta = line[1];
                double a = cos(theta), b = sin(theta);
                double x0 = a*rho, y0 = b*rho;
                double pt1x,pt1y,pt2x,pt2y;
                pt1x = x0 + 1000*(-b);
                pt1y = y0 + 1000*(a);
                pt2x = x0 - 1000*(-b);
                pt2y = y0 - 1000*(a);
                double M,B;
                if (fabs(pt1x-pt2x) > fabs(pt1y-pt2y))
                {
		    //the line is roughly horizontal
                    M = (pt1y-pt2y)/(pt1x-pt2x);
                    B = M*(0-pt2x)+pt2y;
                   rho2tmp[rho2tmpcount++] = B;
                   //cvCircle(frame,cvPoint(0,B),5,cvScalar(0,255,255,0),1,8,0);
	           //printf("rho2 line[%d] M = %f B = %f is horizontal \n",i,M,B);
                } else if( (int)(pt1x-pt2x) == 0) {
		    //the line is exactly vertical
                    //cvCircle(frame,cvPoint(pt1x,0),5,cvScalar(0,255,255,0),1,8,0);
	            //printf("rho2 line[%d] is exactly vertical\n",i);
                    rho2tmp[rho2tmpcount++] = pt1x;
                } else {
		    //the line is roughly vertical
                    M = (pt1y-pt2y)/(pt1x-pt2x);
                    B = M*(0-pt2x)+pt2y;
		    rho2tmp[rho2tmpcount++] = -B/M;
                    //cvCircle(frame,cvPoint(-B/M,0),5,cvScalar(0,255,255,0),1,8,0);
	            //printf("rho2 line[%d] M = %f B = %f -B/M = %f is vertical \n",i,M,B, -B/M);
                }
            }
            issorted = 0;
            while (!issorted)
            {
                    issorted=1;
	            for(i=0;i<rhocount2-1;i++)
	            {
	                if (rho2tmp[i] < rho2tmp[i+1])
	                {
                            issorted=0;
	                    double tmp = rho2tmp[i];
	                    rho2tmp[i] = rho2tmp[i+1];
	                    rho2tmp[i+1] = tmp;
			    int tmprho = rho2[i];
			    rho2[i] = rho2[i+1];
			    rho2[i+1] = tmprho;
	                }
	            }
             }

            //Find intersections of all lines in rho1 with each line in rho2
            for (i=0;i<rhocount1;i++)
            {
                line = (float*)cvGetSeqElem(lines,rho1[i]);
                float rho = line[0];
                float theta = line[1];
                double a = cos(theta), b = sin(theta);
                double x0 = a*rho, y0 = b*rho;
                double pt1x,pt1y,pt2x,pt2y;
                pt1x = x0 + 1000*(-b);
                pt1y = y0 + 1000*(a);
                pt2x = x0 - 1000*(-b);
                pt2y = y0 - 1000*(a);
                int j;
                for(j=0;j<rhocount2;j++)
                {
                    float* line2 = (float*)cvGetSeqElem(lines,rho2[j]);
                    float rho2 = line2[0];
                    float theta2 = line2[1];
                    double a2 = cos(theta2), b2 = sin(theta2);
                    double x02 = a2*rho2, y02 = b2*rho2;
                    double pt3x,pt3y,pt4x,pt4y;
                    pt3x = x02 + 1000*(-b2);
                    pt3y = y02 + 1000*(a2);
                    pt4x = x02 - 1000*(-b2);
                    pt4y = y02 - 1000*(a2);
                    CvPoint mid;
                    double M1,M2,B1,B2;
                    if ((pt1x-pt2x!=0)&&(pt3x-pt4x!=0))
                    {
                        //Not a vertical line
			if(fabs(pt1x-pt2x)>fabs(pt3x-pt4x)){
                            M1 = (pt1y-pt2y)/(pt1x-pt2x);
                            M2 = (pt3y-pt4y)/(pt3x-pt4x);
                            B1 = M1*(0-pt1x)+pt1y;
                            B2 = M2*(0-pt3x)+pt3y;
                            mid.x = (B2-B1)/(M1-M2);
                            mid.y = M1*(mid.x) + B1;
		        }else{
                            M1 = (pt1y-pt2y)/(pt1x-pt2x);
                            M2 = (pt3y-pt4y)/(pt3x-pt4x);
                            B1 = M1*(0-pt1x)+pt1y;
                            B2 = M2*(0-pt3x)+pt3y;
                            mid.x = (B2-B1)/(M1-M2);
                            mid.y = M2*(mid.x) + B2;
			}
                    } else if (pt1x-pt2x==0) {
                        //First line is verical
                        M2 = (pt3y-pt4y)/(pt3x-pt4x);
                        B2 = M2*(0-pt3x)+pt3y;
                        mid.x = pt1x;
                        mid.y = M2*(mid.x) + B2;
                    } else {
                        //Seconds line is verical
                        M1 = (pt1y-pt2y)/(pt1x-pt2x);
                        B1 = M1*(0-pt2x)+pt2y;
                        mid.x = pt3x;
                        mid.y = M1*(mid.x) + B1;
                    }
                    intersects[intersectcount++] = mid;
                }
            }
	    //assign all points to appropriate regions NOTE: TOP LEFT BOTTOM AND RIGHT ARE ALL GENERALIZED AND RELATIVE ONLY
	    grid->rows = rhocount1-1 >=0?rhocount1-1:0; //number of rows of regions
	    grid->columns = rhocount2-1 >=0?rhocount2-1:0; //number of columns of regions
            if(grid->rows*grid->columns != 0){
    	        grid->region = (REGION**)cvAlloc(grid->rows*sizeof(REGION)); //initialize regions
	        for(i=0;i<grid->rows;i++)
		    grid->region[i]= (REGION*)cvAlloc(grid->columns*sizeof(REGION));
	    }
	    int pos=0;
	    for(i=0;i<rhocount1;i++){//cycle rows of intersections
		if(grid->rows*grid->columns == 0) break;
		for(j=0;j<rhocount2;j++){//cycle columns of intersections
		    pos = i*rhocount2 + j; //update the intersection we are assigning
		    if(i==0){ //we are on the very top line so assign to regions below us only
			if(j==0){ //top left corener, only belongs to one region
		    	 	grid->region[0][0].pt[0]=intersects[pos];
			}else if(j<grid->columns){//top middle intersection, belongs to two regions
		    	 	grid->region[0][j-1].pt[j%2]=intersects[pos];
				grid->region[0][j].pt[j%2]=intersects[pos];
			}else{//top end corner, only belongs to one region
				grid->region[0][j-1].pt[j%2]=intersects[pos];
			}
		    }else if(i<grid->rows){ //we are on a middle intersection, so assign to regions both above and below
			if(j==0){//edge, belongs to two regions
		    	 	grid->region[(i-1)][0].pt[2]=intersects[pos]; //region above us
		    	 	grid->region[(i)][0].pt[0]=intersects[pos]; //region below us
			}else if(j<grid->columns){ //central corener, belongs to all four surrounding regions
		    	 	grid->region[(i-1)][j].pt[j%2+2]=intersects[pos];
				grid->region[(i-1)][j-1].pt[j%2+2]=intersects[pos];
				grid->region[(i)][j].pt[j%2]=intersects[pos];
				grid->region[(i)][j-1].pt[j%2]=intersects[pos];
			}else{ //edge, belongs to top bootom and regino behind us
				grid->region[(i)][j-1].pt[j%2]=intersects[pos];
		    	 	grid->region[(i-1)][j-1].pt[j%2+2]=intersects[pos];
			}
		    }else{ //we are on the very bottom line, so assign to regions above us only
			if(j==0){ //bottom left corener, only belongs to one region
		    	 	grid->region[(i-1)][0].pt[2]=intersects[pos];
			}else if(j<grid->columns){//bottom middle corner, belongs to two regions
		    	 	grid->region[(i-1)][j-1].pt[j%2+2]=intersects[pos];
				grid->region[(i-1)][j].pt[j%2+2]=intersects[pos];
			}else{//bottom end corner, only belongs to one region
				grid->region[(i-1)][j-1].pt[j%2+2]=intersects[pos];
			}
		    }
		}
	   }

	//find the top two and bottom two pixels. put the top two in 0&1, the bottom two in 2&3
	for(i=0;i<grid->rows;i++){
	    for(j=0;j<grid->columns;j++){
		grid->region[i][j].type = 0;
		grid->region[i][j].mid.x = 0;
		grid->region[i][j].mid.y = 0;
		CvPoint temp;
		int top1=0,top2=-1,low1=-1,low2=0;
                for (k=0; k<4; k++)
                {
                    // Find top1, the top most corner
                    if (grid->region[i][j].pt[top1].y < grid->region[i][j].pt[k].y)
                        top1 = k;
                    // Find low2, the bottom most corner
                    if (grid->region[i][j].pt[low2].y > grid->region[i][j].pt[k].y)
                        low2 = k;
                }

                // Now we find the middle two
                for (k=0; k<4; k++)
                {
                    if (k != top1 && k != low2)
                    {
                        if (top2 == -1)
                            top2 = k;
                        else
                            low1 = k;
                    }
                }
                // Switch the middle two if needed
		int tmp;
                if (grid->region[i][j].pt[top2].y < grid->region[i][j].pt[low1].y)
                {
                    tmp = top2;
                    top2 = low1;
                    low1 = tmp;
                }

		if(grid->region[i][j].pt[top2].x < grid->region[i][j].pt[top1].x){
		    tmp = top1; //if needed, switch to correctly order x values
		    top1 = top2;
		    top2 = tmp;
		}
		if(grid->region[i][j].pt[low2].x < grid->region[i][j].pt[low1].x){
		    tmp = low1;
		    low1 = low2;
		    low2 = tmp;
		}
		CvPoint pt0 = grid->region[i][j].pt[top1];
		CvPoint pt1 = grid->region[i][j].pt[top2];
		CvPoint pt2 = grid->region[i][j].pt[low1];
		CvPoint pt3 = grid->region[i][j].pt[low2];
		grid->region[i][j].pt[0] = pt0;
		grid->region[i][j].pt[1] = pt1;
		grid->region[i][j].pt[2] = pt2;
		grid->region[i][j].pt[3] = pt3;

	    }
	}

     	#ifdef debug_grid
            IplImage* display = cvCreateImage(cvGetSize(frame),8,3);
            cvCopy(frame, display, 0);

		//NOW FOR DEBUGGING PURPOSES, FILL AREA WITH BLACK
		for(i=0;i<grid->rows;i++){
		    for(j=0;j<grid->columns;j++){
			//line 1 (top)
		        float M1 = (float)(grid->region[i][j].pt[0].y-grid->region[i][j].pt[1].y)/(grid->region[i][j].pt[0].x-grid->region[i][j].pt[1].x);
		        float T1 = (float)M1*grid->region[i][j].pt[0].x-grid->region[i][j].pt[0].y;
			//line 2 (bottom)
		        float M2 = (float)(grid->region[i][j].pt[2].y-grid->region[i][j].pt[3].y)/(grid->region[i][j].pt[2].x-grid->region[i][j].pt[3].x);
		        float T2 = (float)M2*grid->region[i][j].pt[2].x-grid->region[i][j].pt[2].y;
			//line 3 (left)
			float M3;
			if(grid->region[i][j].pt[0].x - grid->region[i][j].pt[2].x != 0){
		            M3 = (float)(grid->region[i][j].pt[0].y-grid->region[i][j].pt[2].y)/(grid->region[i][j].pt[0].x-grid->region[i][j].pt[2].x);
			}else{
			    M3 = 10000;
			}
		        float T3 = (float)M3*grid->region[i][j].pt[0].x-grid->region[i][j].pt[0].y;
			//line 4 (right)
			float M4;
			if(grid->region[i][j].pt[1].x - grid->region[i][j].pt[3].x != 0){
		            M4 = (float)(grid->region[i][j].pt[1].y-grid->region[i][j].pt[3].y)/(grid->region[i][j].pt[1].x-grid->region[i][j].pt[3].x);
			}else{
			    M4 = 10000;
			}
		        float T4 = (float)M4*grid->region[i][j].pt[1].x-grid->region[i][j].pt[1].y;
	
			//find highest and lowest pixel
		  	int top_pix = grid->region[i][j].pt[0].y > grid->region[i][j].pt[1].y ? 0 : 1;
			int low_pix = grid->region[i][j].pt[2].y < grid->region[i][j].pt[3].y ? 2 : 3;
			//cycle down through the three combinations of lines (1 & 2 will never share y values)
			int y,x;
			uchar* ptr;

			grid->region[i][j].avgg= 0x00;
			grid->region[i][j].avgr= 0x00;
			grid->region[i][j].avgb= 0x00;

			for(y=grid->region[i][j].pt[top_pix].y; y>grid->region[i][j].pt[(top_pix+1)%2].y;y--){
			    if(y < 0 || y>= frame->height) continue; //don't attempt to access anything off the screen
			    if(M1==0){ 
				break;//we can skip to the middle section
			    }
			    if(top_pix == 0){ //work from line 3 to line 1
	       			 ptr = (uchar*) (display->imageData + y * display->widthStep);  
				for(x=(int)(y+T3)/M3;x<(int)(y+T1)/M1;x++){
			    	   if(x < 0 || x>= frame->width) continue; //don't attempt to access anything off the screen
				   ptr[3*x+0] = grid->region[i][j].avgb;
				   ptr[3*x+1] = grid->region[i][j].avgg;
				   ptr[3*x+2] = grid->region[i][j].avgr;
				}
			    }else{            //work from line 1 to line 4
	       			 ptr = (uchar*) (display->imageData + y * display->widthStep);   
				for(x=(int)(y+T1)/M1;x<(int)((y+T4)/M4);x++){
			    	   if(x < 0 || x>= frame->width) continue; //don't attempt to access anything off the screen
				   ptr[3*x+0] = grid->region[i][j].avgb;
				   ptr[3*x+1] = grid->region[i][j].avgg;
				   ptr[3*x+2] = grid->region[i][j].avgr;
				}
			    }
			}
			for(y=grid->region[i][j].pt[(top_pix+1)%2].y; y>grid->region[i][j].pt[(low_pix-1)%2+2].y;y--){
			    if(y < 0 || y>= frame->height) continue; //don't attempt to access anything off the screen
			    //work from line 3 to line 4
	       		     ptr = (uchar*) (display->imageData + y * display->widthStep); 
			    for(x=(int)(y+T3)/M3;x<(int)(y+T4)/M4;x++){
			    	   if(x < 0 || x>= frame->width) continue; //don't attempt to access anything off the screen
				   ptr[3*x+0] = grid->region[i][j].avgb;
				   ptr[3*x+1] = grid->region[i][j].avgg;
				   ptr[3*x+2] = grid->region[i][j].avgr;
			    }
			}
			for(y=grid->region[i][j].pt[(low_pix-1)%2+2].y; y>grid->region[i][j].pt[low_pix].y;y--){
			    if(y < 0 || y>= frame->height) continue; //don't attempt to access anything off the screen
			    if(M2 == 0) break; //we are done, the bottom line is flat
			    if(low_pix == 2){ //work from line 3 to line 2
	       		         ptr = (uchar*) (display->imageData + y * display->widthStep); 
				for(x=(int)(y+T3)/M3;x<(int)(y+T2)/M2;x++){
			    	   if(x < 0 || x>= frame->width) continue; //don't attempt to access anything off the screen
				   ptr[3*x+0] = grid->region[i][j].avgb;
				   ptr[3*x+1] = grid->region[i][j].avgg;
				   ptr[3*x+2] = grid->region[i][j].avgr;
				}
			    }else{            //work form line 2 to line 4
	       		         ptr = (uchar*) (display->imageData + y * display->widthStep); 
				for(x=(int)(y+T2)/M2;x<(int)(y+T4)/M4;x++){
			    	   if(x < 0 || x>= frame->width) continue; //don't attempt to access anything off the screen
				   ptr[3*x+0] = grid->region[i][j].avgb;
				   ptr[3*x+1] = grid->region[i][j].avgg;
				   ptr[3*x+2] = grid->region[i][j].avgr;
				}
			    }
			}
		    }
		}

            //Display Intersections
            for(i=0;i<intersectcount;i++)
            {
                CvPoint mid = intersects[i];
                cvCircle(display,mid,5,cvScalar(255,0,0,0),1,8,0);  
            }
	    //Display regions
	    for(i=0;i<grid->rows;i++){
		for(j=0;j<grid->columns;j++){
		    double avgx=0;	
		    double avgy=0;
		    for(k=0;k<4;k++){
		        avgx += grid->region[i][j].pt[k].x;
		        avgy += grid->region[i][j].pt[k].y;
		    }
		    avgx /= 4;
		    avgy /=4;
		    cvCircle(display,cvPoint((int)avgx,(int)avgy),5,cvScalar(0,0,255,0),1,8,0);    
		}
	    }
   	    cvShowImage("Grid",display);
	    cvReleaseImage(&display);
	#endif

	
}

/*
void find_bins(GRID* grid, IplImage* frame) {

	Image* rgb_tmp =NULL;
	Image* indexed_tmp = NULL;
	Image* red_filter=NULL;
	Image* black_filter=NULL;
	RGBPixel color;
	int flaggedPix[grid->rows][grid->columns]; //accumulates number of pixels flagged for each regions
	IplImage* ipl_out;
	

	ipl_out = cvCreateImage(cvSize(frame->width,frame->height), 8, 3);
        rgb_tmp = Image_new(RGB, frame->width, frame->height);
        red_filter = Image_new(RGB, frame->width, frame->height);
        black_filter = Image_new(RGB, frame->width, frame->height);
        indexed_tmp = Image_new(INDEXED, frame->width, frame->height);

	//run a color filter on frame looking for red
	color.r = 0xff;
	color.b = 0x00;
	color.g = 0x00;

        IplImageToImage(frame, rgb_tmp);
        FindTargetColor(rgb_tmp, indexed_tmp, &color, 80,220);
        Image_indexedToRGB(indexed_tmp, red_filter); 
        cvNamedWindow("Red",CV_WINDOW_AUTOSIZE); 
             ImageToIplImage(red_filter, ipl_out);//temporary!!
	cvShowImage("Red", ipl_out);

	//run a color filter on frame looking for black
	color.r = 0x00;
	color.b = 0x00;
	color.g = 0x00;

        IplImageToImage(frame, rgb_tmp);
        FindTargetColor(rgb_tmp, indexed_tmp, &color, 80,220);
        Image_indexedToRGB(indexed_tmp, black_filter); 
        cvNamedWindow("Black",CV_WINDOW_AUTOSIZE); 
             ImageToIplImage(black_filter, ipl_out);//temporary!
	cvShowImage("Black",ipl_out);

	int i,j;

	//Find the number of red or black pixels (flagged pixels) in each bin, and the area of each bin
	for(i=0;i<grid->rows;i++){
	    for(j=0;j<grid->columns;j++){
		//line 1 (top)
                float M1 = (float)(grid->region[i][j].pt[0].y-grid->region[i][j].pt[1].y)/(grid->region[i][j].pt[0].x-grid->region[i][j].pt[1].x);
                float T1 = (float)M1*grid->region[i][j].pt[0].x-grid->region[i][j].pt[0].y;
		//line 2 (bottom)
                float M2 = (float)(grid->region[i][j].pt[2].y-grid->region[i][j].pt[3].y)/(grid->region[i][j].pt[2].x-grid->region[i][j].pt[3].x);
                float T2 = (float)M2*grid->region[i][j].pt[2].x-grid->region[i][j].pt[2].y;
		//line 3 (left)
		float M3;
		if(grid->region[i][j].pt[0].x - grid->region[i][j].pt[2].x != 0){
                    M3 = (float)(grid->region[i][j].pt[0].y-grid->region[i][j].pt[2].y)/(grid->region[i][j].pt[0].x-grid->region[i][j].pt[2].x);
		}else{
		    M3 = 10000;
		}
                float T3 = (float)M3*grid->region[i][j].pt[0].x-grid->region[i][j].pt[0].y;
		//line 4 (right)
		float M4;
		if(grid->region[i][j].pt[1].x - grid->region[i][j].pt[3].x != 0){
                    M4 = (float)(grid->region[i][j].pt[1].y-grid->region[i][j].pt[3].y)/(grid->region[i][j].pt[1].x-grid->region[i][j].pt[3].x);
		}else{
		    M4 = 10000;
		}
                float T4 = (float)M4*grid->region[i][j].pt[1].x-grid->region[i][j].pt[1].y;

		//make sure all colors and such are set to zero
		grid->region[i][j].avgb = 0;
		grid->region[i][j].avgg = 0;
		grid->region[i][j].avgr = 0;
		grid->region[i][j].area = 0;
		grid->region[i][j].type = 0;
		flaggedPix[i][j] = 0;
	
		//find highest and lowest pixel
	  	int top_pix = grid->region[i][j].pt[0].y > grid->region[i][j].pt[1].y ? 0 : 1;
		int low_pix = grid->region[i][j].pt[2].y < grid->region[i][j].pt[3].y ? 2 : 3;
		//cycle down through the three combinations of lines (1 & 2 will never share y values)
		int y,x;
		uchar* ptr;
		for(y=grid->region[i][j].pt[top_pix].y; y>grid->region[i][j].pt[(top_pix+1)%2].y;y--){
		    if(y < 0 || y>= frame->height) continue; //don't attempt to access anything off the screen
		    if(M1==0){ 
			break;//we can skip to the middle section
		    }
		    if(top_pix == 0){ //work from line 3 to line 1
       			ptr = (uchar*) (frame->imageData + y * frame->widthStep);  
			for(x=(int)(y+T3)/M3;x<(int)(y+T1)/M1;x++){
		    	   if(x < 0 || x>= frame->width) continue; //don't attempt to access anything off the screen
			   //if red_filter or black_filter have highlighted this pixel, increase flaggedPix
        		   if(red_filter->data.rgb[y*(frame->widthStep/3)+x].r > 0 || black_filter->data.rgb[y*(frame->widthStep/3)+x].r > 0){
			      flaggedPix[i][j]++;
			   }
			   grid->region[i][j].avgr += ptr[3*x+2];
			   grid->region[i][j].avgg += ptr[3*x+1];
			   grid->region[i][j].avgb += ptr[3*x+0];
			   grid->region[i][j].area++;
			}
		    }else{            //work from line 1 to line 4
       			 ptr = (uchar*) (frame->imageData + y * frame->widthStep);   
			for(x=(int)(y+T1)/M1;x<(int)((y+T4)/M4);x++){
		    	   if(x < 0 || x>= frame->width) continue; //don't attempt to access anything off the screen
			   //if red_filter or black_filter have highlighted this pixel, increase flaggedPix
        		   if(red_filter->data.rgb[y*(frame->widthStep/3)+x].r > 0 || black_filter->data.rgb[y*(frame->widthStep/3)+x].r > 0){
			      flaggedPix[i][j]++;
			   }
			   grid->region[i][j].avgr += ptr[3*x+2];
			   grid->region[i][j].avgg += ptr[3*x+1];
			   grid->region[i][j].avgb += ptr[3*x+0];
			   grid->region[i][j].area++;
			}
		    }
		}
		for(y=grid->region[i][j].pt[(top_pix+1)%2].y; y>grid->region[i][j].pt[(low_pix-1)%2+2].y;y--){
		    if(y < 0 || y>= frame->height) continue; //don't attempt to access anything off the screen
		    //work from line 3 to line 4
       		     ptr = (uchar*) (frame->imageData + y * frame->widthStep); 
		    for(x=(int)(y+T3)/M3;x<(int)(y+T4)/M4;x++){
		    	   if(x < 0 || x>= frame->width) continue; //don't attempt to access anything off the screen
			   //if red_filter or black_filter have highlighted this pixel, increase flaggedPix
        		   if(red_filter->data.rgb[y*(frame->widthStep/3)+x].r > 0 || black_filter->data.rgb[y*(frame->widthStep/3)+x].r > 0){
			      flaggedPix[i][j]++;
			   }
			   grid->region[i][j].avgr += ptr[3*x+2];
			   grid->region[i][j].avgg += ptr[3*x+1];
			   grid->region[i][j].avgb += ptr[3*x+0];
			   grid->region[i][j].area++;
		    }
		}
		for(y=grid->region[i][j].pt[(low_pix-1)%2+2].y; y>grid->region[i][j].pt[low_pix].y;y--){
		    if(y < 0 || y>= frame->height) continue; //don't attempt to access anything off the screen
		    if(M2 == 0) break; //we are done, the bottom line is flat
		    if(low_pix == 2){ //work from line 3 to line 2
       		         ptr = (uchar*) (frame->imageData + y * frame->widthStep); 
		        for(x=(int)(y+T3)/M3;x<(int)(y+T2)/M2;x++){
		    	   if(x < 0 || x>= frame->width) continue; //don't attempt to access anything off the screen
			   //if red_filter or black_filter have highlighted this pixel, increase flaggedPix
        		   if(red_filter->data.rgb[y*(frame->widthStep/3)+x].r > 0 || black_filter->data.rgb[y*(frame->widthStep/3)+x].r > 0){
			      flaggedPix[i][j]++;
			   }
			   grid->region[i][j].avgr += ptr[3*x+2];
			   grid->region[i][j].avgg += ptr[3*x+1];
			   grid->region[i][j].avgb += ptr[3*x+0];
			   grid->region[i][j].area++;
		        }
		    }else{            //work form line 2 to line 4
       		         ptr = (uchar*) (frame->imageData + y * frame->widthStep); 
		        for(x=(int)(y+T2)/M2;x<(int)(y+T4)/M4;x++){
		    	   if(x < 0 || x>= frame->width) continue; //don't attempt to access anything off the screen
			   //if red_filter or black_filter have highlighted this pixel, increase flaggedPix
        		   if(red_filter->data.rgb[y*(frame->widthStep/3)+x].r > 0 || black_filter->data.rgb[y*(frame->widthStep/3)+x].r > 0){
			      flaggedPix[i][j]++;
			   }
			   grid->region[i][j].avgr += ptr[3*x+2];
			   grid->region[i][j].avgg += ptr[3*x+1];
			   grid->region[i][j].avgb += ptr[3*x+0];
			   grid->region[i][j].area++;
		        }
		    }
		}
		grid->region[i][j].avgr /= grid->region[i][j].area;
		grid->region[i][j].avgb /= grid->region[i][j].area;
		grid->region[i][j].avgg /= grid->region[i][j].area;
	    }
	} //done finding average color & area


    //find the average brighntess of the image (looking for black, so color is irelevent really)
    unsigned int avg_red = 0; 
    unsigned int avg_blue = 0;
    for(int i = frame->height * frame->width - 1; i >= 0; i--) {
        avg_red += (unsigned char)frame->imageData[(3 * i) + 2];
        avg_blue += (unsigned char)frame->imageData[(3 * i) + 0];
        //avg_green += (unsigned char)frame->imageData[(3 * i) + 1];
    }
    avg_red = (unsigned int)(avg_red/((float)(frame->width*frame->height)));
    avg_blue = (unsigned int)(avg_blue/((float)(frame->width*frame->height)));

    //flag all regions that are probably bins (type = 5: it's a bin, but we don't know what type yet)
    for(i=0;i<grid->rows;i++){
	for(j=0;j<grid->columns;j++){
	    //if the ratio of flagged to unflaged pixels in each region is greater than a threshold, make that region a bin
	    if((float)flaggedPix[i][j]/(float)grid->region[i][j].area > 2.0/3.0){ 
		grid->region[i][j].type = 5;
	    }
	}
    }

    //release images
    cvReleaseImage(&ipl_out);
    Image_destroy(rgb_tmp);
    Image_destroy(indexed_tmp);
    Image_destroy(red_filter);
    Image_destroy(black_filter);
}

void combine_bins(GRID* grid, IplImage* frame){
    //Method:
    //sweep the image once along each row, and then once along each column, 
    //combining two bins by turning the second into a non-bin, and giving
    // the first the latter's right most or bottom most points
    //

    int i,j,k,l;
    int was_bin=0;//wether or not the last bin that was check was a bin

    //PASS THROUGH EVERY ROW
    for(i=0;i<grid->rows;i++){
	was_bin=0;
	for(j=0;j<grid->columns;j++){
	    //if this is a bin, and the last region was a bin
	    if(was_bin && grid->region[i][j].type){
		grid->region[i][j-1].type = 0;
		for(k=0;k<4;k++){
		    for(l=0;l<4;l++){
    		        if(grid->region[i][j].pt[k].x == grid->region[i][j-1].pt[l].x &&
		           grid->region[i][j].pt[k].y == grid->region[i][j-1].pt[l].y){

			    grid->region[i][j].pt[k] = grid->region[i][j-1].pt[k];
			    break;
 		        }
		    }
		}
                //printf("combining two columns\n");
		was_bin = 1;
	    }else{
		was_bin = grid->region[i][j].type;
	    }
	}
    }

    //PASS THROUGH EVERY COLUMN
    for(j=0;j<grid->columns;j++){
	was_bin=0;
	for(i=0;i<grid->rows;i++){
	    //if this is a bin, and the last region was a bin
	    if(was_bin && grid->region[i][j].type){
		grid->region[i-1][j].type = 0;	
		//enlarge the first reason with the two new corners	
		for(k=0;k<4;k++){
		    for(l=0;l<4;l++){
		        if(grid->region[i][j].pt[k].x == grid->region[i-1][j].pt[l].x &&
		           grid->region[i][j].pt[k].y == grid->region[i-1][j].pt[l]. y){

			    grid->region[i][j].pt[k] = grid->region[i-1][j].pt[k];
			    break;
		        }
		    }
		}
                //printf("combining two rows\n");
		was_bin = 1;
	    }else{
		was_bin = grid->region[i][j].type;
	    }
	}
    }

     	#ifdef debug_grid
            cvNamedWindow("combined", CV_WINDOW_AUTOSIZE);
            IplImage* display = cvCreateImage(cvGetSize(frame),8,3);
            cvCopy(frame, display, 0);

		//NOW FOR DEBUGGING PURPOSES, FILL AREA WITH BLACK
		for(i=0;i<grid->rows;i++){
		    for(j=0;j<grid->columns;j++){
			if(grid->region[i][j].type == 0) continue;
			//line 1 (top)
		        float M1 = (float)(grid->region[i][j].pt[0].y-grid->region[i][j].pt[1].y)/(grid->region[i][j].pt[0].x-grid->region[i][j].pt[1].x);
		        float T1 = (float)M1*grid->region[i][j].pt[0].x-grid->region[i][j].pt[0].y;
			//line 2 (bottom)
		        float M2 = (float)(grid->region[i][j].pt[2].y-grid->region[i][j].pt[3].y)/(grid->region[i][j].pt[2].x-grid->region[i][j].pt[3].x);
		        float T2 = (float)M2*grid->region[i][j].pt[2].x-grid->region[i][j].pt[2].y;
			//line 3 (left)
			float M3;
			if(grid->region[i][j].pt[0].x - grid->region[i][j].pt[2].x != 0){
		            M3 = (float)(grid->region[i][j].pt[0].y-grid->region[i][j].pt[2].y)/(grid->region[i][j].pt[0].x-grid->region[i][j].pt[2].x);
			}else{
			    M3 = 10000;
			}
		        float T3 = (float)M3*grid->region[i][j].pt[0].x-grid->region[i][j].pt[0].y;
			//line 4 (right)
			float M4;
			if(grid->region[i][j].pt[1].x - grid->region[i][j].pt[3].x != 0){
		            M4 = (float)(grid->region[i][j].pt[1].y-grid->region[i][j].pt[3].y)/(grid->region[i][j].pt[1].x-grid->region[i][j].pt[3].x);
			}else{
			    M4 = 10000;
			}
		        float T4 = (float)M4*grid->region[i][j].pt[1].x-grid->region[i][j].pt[1].y;
	
			//find highest and lowest pixel
		  	int top_pix = grid->region[i][j].pt[0].y > grid->region[i][j].pt[1].y ? 0 : 1;
			int low_pix = grid->region[i][j].pt[2].y < grid->region[i][j].pt[3].y ? 2 : 3;
			//cycle down through the three combinations of lines (1 & 2 will never share y values)
			int y,x;
			uchar* ptr;

			grid->region[i][j].avgg= 0x00;
			grid->region[i][j].avgr= 0x00;
			grid->region[i][j].avgb= 0x00;

			for(y=grid->region[i][j].pt[top_pix].y; y>grid->region[i][j].pt[(top_pix+1)%2].y;y--){
			    if(y < 0 || y>= frame->height) continue; //don't attempt to access anything off the screen
			    if(M1==0){ 
				break;//we can skip to the middle section
			    }
			    if(top_pix == 0){ //work from line 3 to line 1
	       			 ptr = (uchar*) (display->imageData + y * display->widthStep);  
				for(x=(int)(y+T3)/M3;x<(int)(y+T1)/M1;x++){
			    	   if(x < 0 || x>= frame->width) continue; //don't attempt to access anything off the screen
				   ptr[3*x+0] = grid->region[i][j].avgb;
				   ptr[3*x+1] = grid->region[i][j].avgg;
				   ptr[3*x+2] = grid->region[i][j].avgr;
				}
			    }else{            //work from line 1 to line 4
	       			 ptr = (uchar*) (display->imageData + y * display->widthStep);   
				for(x=(int)(y+T1)/M1;x<(int)((y+T4)/M4);x++){
			    	   if(x < 0 || x>= frame->width) continue; //don't attempt to access anything off the screen
				   ptr[3*x+0] = grid->region[i][j].avgb;
				   ptr[3*x+1] = grid->region[i][j].avgg;
				   ptr[3*x+2] = grid->region[i][j].avgr;
				}
			    }
			}
			for(y=grid->region[i][j].pt[(top_pix+1)%2].y; y>grid->region[i][j].pt[(low_pix-1)%2+2].y;y--){
			    if(y < 0 || y>= frame->height) continue; //don't attempt to access anything off the screen
			    //work from line 3 to line 4
	       		     ptr = (uchar*) (display->imageData + y * display->widthStep); 
			    for(x=(int)(y+T3)/M3;x<(int)(y+T4)/M4;x++){
			    	   if(x < 0 || x>= frame->width) continue; //don't attempt to access anything off the screen
				   ptr[3*x+0] = grid->region[i][j].avgb;
				   ptr[3*x+1] = grid->region[i][j].avgg;
				   ptr[3*x+2] = grid->region[i][j].avgr;
			    }
			}
			for(y=grid->region[i][j].pt[(low_pix-1)%2+2].y; y>grid->region[i][j].pt[low_pix].y;y--){
			    if(y < 0 || y>= frame->height) continue; //don't attempt to access anything off the screen
			    if(M2 == 0) break; //we are done, the bottom line is flat
			    if(low_pix == 2){ //work from line 3 to line 2
	       		         ptr = (uchar*) (display->imageData + y * display->widthStep); 
				for(x=(int)(y+T3)/M3;x<(int)(y+T2)/M2;x++){
			    	   if(x < 0 || x>= frame->width) continue; //don't attempt to access anything off the screen
				   ptr[3*x+0] = grid->region[i][j].avgb;
				   ptr[3*x+1] = grid->region[i][j].avgg;
				   ptr[3*x+2] = grid->region[i][j].avgr;
				}
			    }else{            //work form line 2 to line 4
	       		         ptr = (uchar*) (display->imageData + y * display->widthStep); 
				for(x=(int)(y+T2)/M2;x<(int)(y+T4)/M4;x++){
			    	   if(x < 0 || x>= frame->width) continue; //don't attempt to access anything off the screen
				   ptr[3*x+0] = grid->region[i][j].avgb;
				   ptr[3*x+1] = grid->region[i][j].avgg;
				   ptr[3*x+2] = grid->region[i][j].avgr;
				}
			    }
			}
		    }
		}

	    //Display regions
	    for(i=0;i<grid->rows;i++){
		for(j=0;j<grid->columns;j++){
		    if(grid->region[i][j].type ==0) continue;
		    double avgx=0;	
		    double avgy=0;
		    for(k=0;k<4;k++){
		        avgx += grid->region[i][j].pt[k].x;
		        avgy += grid->region[i][j].pt[k].y;
		    }
		    avgx /= 4;
		    avgy /=4;
		    cvCircle(display,cvPoint((int)avgx,(int)avgy),5,cvScalar(0,0,255,0),1,8,0);    
		}
	    }
   	    cvShowImage("combined",display);
	    cvReleaseImage(&display);
	#endif
}

void determine_type(GRID* grid, IplImage* frame){
    //create a new image to run analyzation in ,and copy over the region onto a *black* background (we can adjust background color later)
    IplImage* isolated = cvCreateImage(cvGetSize(frame),8,3);
    int i,j,x,y,k,l=0;
    for(i=0;i<grid->rows;i++){
	for(j=0;j<grid->columns;j++){
	    if(grid->region[i][j].type != 5) continue;
		//line 1 (top)
                float M1 = (float)(grid->region[i][j].pt[0].y-grid->region[i][j].pt[1].y)/(grid->region[i][j].pt[0].x-grid->region[i][j].pt[1].x);
                float T1 = (float)M1*grid->region[i][j].pt[0].x-grid->region[i][j].pt[0].y;
		//line 2 (bottom)
                float M2 = (float)(grid->region[i][j].pt[2].y-grid->region[i][j].pt[3].y)/(grid->region[i][j].pt[2].x-grid->region[i][j].pt[3].x);
                float T2 = (float)M2*grid->region[i][j].pt[2].x-grid->region[i][j].pt[2].y;
		//line 3 (left)
		float M3;
		if(grid->region[i][j].pt[0].x - grid->region[i][j].pt[2].x != 0){
                    M3 = (float)(grid->region[i][j].pt[0].y-grid->region[i][j].pt[2].y)/(grid->region[i][j].pt[0].x-grid->region[i][j].pt[2].x);
		}else{
		    M3 = 10000;
		}
                float T3 = (float)M3*grid->region[i][j].pt[0].x-grid->region[i][j].pt[0].y;
		//line 4 (right)
		float M4;
		if(grid->region[i][j].pt[1].x - grid->region[i][j].pt[3].x != 0){
                    M4 = (float)(grid->region[i][j].pt[1].y-grid->region[i][j].pt[3].y)/(grid->region[i][j].pt[1].x-grid->region[i][j].pt[3].x);
		}else{
		    M4 = 10000;
		}
                float T4 = (float)M4*grid->region[i][j].pt[1].x-grid->region[i][j].pt[1].y;
	
		//find highest and lowest pixel
	  	int top_pix = grid->region[i][j].pt[0].y > grid->region[i][j].pt[1].y ? 0 : 1;
		int low_pix = grid->region[i][j].pt[2].y < grid->region[i][j].pt[3].y ? 2 : 3;
		//cycle down through the three combinations of lines (1 & 2 will never share y values)
		uchar* ptr;
		uchar* ptrN;

	    for(y=frame->height-1;y>=0;y--){
	    ptr = (uchar*) (frame->imageData + y * frame->widthStep); 
	    ptrN = (uchar*) (isolated->imageData + y * isolated->widthStep);
		for(x=0;x<frame->width-1;x++){
			int inregion = 0;
			if(y<grid->region[i][j].pt[top_pix].y && y>= grid->region[i][j].pt[(top_pix+1)%2].y && M1 !=0){
			    if(top_pix == 0){ //work from line 3 to line 1 
				if(x>(int)(y+T3)/M3 && x<(int)(y+T1)/M1){
				    inregion = 1;
				}
			    }else{            //work from line 1 to line 4  
				if(x>(int)(y+T1)/M1 && x<(int)(y+T4)/M4){
				    inregion = 1;
				}
			    }
			}else if(y<grid->region[i][j].pt[(top_pix+1)%2].y && y>=grid->region[i][j].pt[(low_pix-1)%2+2].y){
			    //work from line 3 to line 4
			    if(x>(int)(y+T3)/M3 && x<(int)(y+T4)/M4){
				    inregion = 1;
			    }
			}else if(y<grid->region[i][j].pt[(low_pix-1)%2+2].y && y>=grid->region[i][j].pt[low_pix].y && M2 != 0){
			    if(low_pix == 2){ //work from line 3 to line 2
				if(x>(int)(y+T3)/M3 && x<(int)(y+T2)/M2){
				    inregion = 1;
				}
			    }else{            //work form line 2 to line 4
				if(x>(int)(y+T2)/M2 && x<(int)(y+T4)/M4){
				    inregion = 1;
				}
			    }
			}
			if(inregion){
			   ptrN[3*x+0] = ptr[3*x+0];
			   ptrN[3*x+1] = ptr[3*x+1];
			   ptrN[3*x+2] = ptr[3*x+2];
			}else{
			   ptrN[3*x+0] = grid->region[i][j].avgb;
			   ptrN[3*x+1] = grid->region[i][j].avgg;
			   ptrN[3*x+2] = grid->region[i][j].avgr;
			}

		}
	    }  
	    if(1){
		if(l==0){
		    #ifdef debug_bins
			cvShowImage("Bin1",isolated);
		    #endif
		}else if(l==1){
		    #ifdef debug_bins
			cvShowImage("Bin2",isolated);
		    #endif
		}else if(l ==2){
		    #ifdef debug_bins
			cvShowImage("Bin3",isolated);
		    #endif
		}else if(l ==3){
		    #ifdef debug_bins
			cvShowImage("Bin4",isolated);
		    #endif
		}
	    }
	    l++;
	    //we now have an image with nothing but the interior of the bin and a backdrop
	    grid->region[i][j].type = analyze_bin(isolated,grid->region[i][j].area);
	    //printf("bin %d is type %d\n",l,grid->region[i][j].type);
	}
    }
    cvReleaseImage(&isolated);
}

int analyze_bin(IplImage* isolated, int binArea){
    int i;
    int type=0;
    int blobArea;
    float ratio=0;
    float ratios[4] = {.204,.121,.485,.454};//targetsize/binsize for battleship, airplane, factory, tank
    RGBPixel color;
    IplImage* ipl_out=NULL;
    Image* rgb_tmp = NULL;
    Image* indexed_tmp = NULL; 

    //initialize images
    ipl_out = cvCreateImage(cvSize(isolated->width,isolated->height), 8, 3);
    rgb_tmp = Image_new(RGB, isolated->width,isolated->height);
    indexed_tmp = Image_new(INDEXED,isolated->width,isolated->height); 

    //assign target color
    color.r = 0xff;
    color.g = 0x00;
    color.b = 0x00;

    IplImageToImage(isolated, rgb_tmp);
    blobArea = FindTargetColor(rgb_tmp, indexed_tmp, &color, 80, 444);
    Image_indexedToRGB(indexed_tmp, rgb_tmp); 
    ImageToIplImage(rgb_tmp, ipl_out);

    //find closest ratio
    ratio = (float)((float)blobArea)/binArea;
    for(i=0;i<4;i++){
	if(fabs(ratio-ratios[i]) < fabs(ratio-ratios[type]))
	    type = i;
    }

    if(type == 2 || type == 3){ //if it's either a tank or a factory, use hough to decide 
        IplImage* grey;
        IplImage* edge;
        CvSeq* lines; 
	int lineTotal=0;
        float* line = 0;
	int hough_threshold;//make this depend on the size of the bin

        grey = cvCreateImage(cvSize(isolated->width,isolated->height), 8, 1);
        cvCvtColor(ipl_out, grey, CV_BGR2GRAY);
        edge = edge_opencv(grey, 50, 150, 3);
        lines = hough_opencv(edge, isolated, 25, 10, 90,90, 10, 60, 60);
	//count hough lines
	for(i=0;i<10;i++){
            line = (float*)cvGetSeqElem(lines,i);
	    if(line[0] != -999){	    
		lineTotal++;
	    }
	}
	if(lineTotal > 2)
	    type = 2; //lots of lines = prob. a factory
	else
	    type = 3; //not lots of lines = prob. a tank


	cvReleaseImage(&grey);
	cvReleaseImage(&edge);
        cvRelease((void**) &lines);
    }


    printf("blobArea = %d, binArea = %d,ratio = %f, type=%d \n",blobArea,binArea,ratio,type);	

    #ifdef debug_tuna
        cvShowImage("out2", ipl_out);
    #endif 

    //release images
    Image_destroy(rgb_tmp);
    Image_destroy(indexed_tmp);
    cvReleaseImage(&ipl_out);
    return type;
}

*/

void grid_free() {}



