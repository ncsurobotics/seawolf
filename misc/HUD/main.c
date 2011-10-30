/*Seawolf III HUD GUI
 *
 *This program allows the user to check the real-time dynamics of the Seawolf III vehicle
 *
 *Author: R. Brooks Stephenson
 *Version:2009.7.27
 *
 */

#define seawolf

#include "seawolf.h"

#include <stdio.h>
#include <stdlib.h>
#include <X11/X.h>
#include <X11/Xlib.h>
#include <GL/gl.h>
#include <GL/glx.h>
#include <GL/glu.h>
#include <math.h>
#include <string.h>


//Defines
#define PI 3.1415927

#define WINDOW_X 640
#define WINDOW_Y 480
#define SCREEN_X 1024
#define SCREEN_Y 600

//Depth Meter
#define DEPTH_SKY 20
#define DEPTH_GND 20
#define DEPTH_SLDR_OFST 8
#define DEPTH_SLDR_WIDTH 10
#define DEPTH_SLDR_HEIGHT 20
#define DEPTH_METER_MAX 11.0//Set the maximum depth represented on-screen
#define DEPTH_METER_TOP_COLOR 0.7f, 0.7f, 0.7f
#define DEPTH_METER_BOTTOM_COLOR 0.3f , 0.3f, 0.3f


//Level Meter
#define LEVEL_METER_LEFT ((WINDOW_X/3.0)*2.0)
#define LEVEL_METER_RADIUS ((WINDOW_X/3.0)/2.0)
#define LEVEL_METER_CENTER_Y ((WINDOW_Y/4.0)*3.0)


//Plot Defines
#define MAX_PLOTS 8

#define CUR_DEPTH 0
#define CUR_ROLL 1
#define CUR_PITCH 2
#define CUR_YAW 3

#define SET_DEPTH 4
#define SET_ROLL 5
#define SET_PITCH 6
#define SET_YAW 7

#define PLOT_RES 0.5

//Acoustic Plot Defines
#define XRES 10
#define XSPEED 10



//PLOT STRUCTURE
typedef struct _DATA_POINT
{
    float data;
    struct _DATA_POINT *next;
}DATA_POINT;



//Function prototypes
void DrawDepthGuage();
void DrawLevelGuage();
void Text(char* str, int x, int y, int size, int width, float red, float green, float blue);
void UpdatePlot(int plotNum, float data);
void DrawPlots();

//OpenGL Variables
static Display                 *dpy;
static Window                  root;
static GLint                   att[] = { GLX_RGBA, GLX_DEPTH_SIZE, 24, GLX_DOUBLEBUFFER, None };
static XVisualInfo             *vi;
static Colormap                cmap;
static XSetWindowAttributes    swa;
static Window                  win;
static GLXContext              glc;
static XWindowAttributes       gwa;

static float i;
static int numPlotPoints;

static DATA_POINT **plot;

//Heading variable
static float currentRoll;
static float currentPitch;
static float currentYaw;

static float desiredDepth;
static float desiredPitch;
static float desiredYaw;

//Depth variables
static float currentDepth;

void Render()
{
    glClearColor(0.0, 0.0, 0.0, 1.0);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho( 0, WINDOW_X, 0, WINDOW_Y , -20, 20.);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    gluLookAt(0., 0., 10., 0., 0., 0., 0., 1., 0.);


    //Start drawing the HUD
    DrawDepthGuage();
    DrawLevelGuage();
    DrawPlots();
}





int main(int argc, char *argv[])
{

    i=0.0;
    numPlotPoints=0;

    //Allocate memory for the plot
    plot = (DATA_POINT**)calloc( MAX_PLOTS, sizeof(DATA_POINT*));

#ifdef seawolf
    Seawolf_loadConfig("../../conf/seawolf.conf");
    Seawolf_init("HUD");
#endif

    currentDepth=0;

    dpy = XOpenDisplay(NULL);

    if(dpy == NULL)
        {
            printf("\n\tcannot connect to X server\n\n");
            exit(0);
        }

    root = DefaultRootWindow(dpy);

    vi = glXChooseVisual(dpy, 0, att);

    if(vi == NULL)
        {
            printf("\n\tno appropriate visual found\n\n");
            exit(0);
        }
    else
        {
            //printf("\n\tvisual %p selected\n", vi->visualid);
        }/* %p creates hexadecimal output like in glxinfo */


    cmap = XCreateColormap(dpy, root, vi->visual, AllocNone);

    swa.colormap = cmap;
    swa.event_mask = ExposureMask | KeyPressMask;

    win = XCreateWindow(dpy, root, (SCREEN_X-WINDOW_X)/2,(SCREEN_Y-WINDOW_Y)/2 , WINDOW_X, WINDOW_Y, 0, vi->depth, InputOutput, vi->visual, CWColormap | CWEventMask, &swa);

    XMapWindow(dpy, win);
    XStoreName(dpy, win, "Seawolf HUD");

    glc = glXCreateContext(dpy, vi, NULL, GL_TRUE);
    glXMakeCurrent(dpy, win, glc);

    glEnable(GL_DEPTH_TEST);

#ifdef seawolf
    Var_bind("Depth", &currentDepth);
    Var_bind("DepthPID.Heading", &desiredDepth);
    Var_bind("SEA.Roll", &currentRoll);
    Var_bind("SEA.Pitch", &currentPitch);
    Var_bind("SEA.Yaw", &currentYaw);
#endif

    while(1)
        {

#ifdef seawolf
            Util_usleep(0.02);
#else
            currentDepth=10.0*sin(i*PI/180.0);
            currentRoll =180.0*cos(i*PI/180.0) ;
            currentPitch=10.0*sin(i*PI/180.0);
            currentYaw = 180.0*cos((i+90.0)*PI/180.0);

            desiredDepth=4*cos(i*PI/180.0);
            desiredPitch=180.0*sin((i+30.0f)*PI/180.0);
            desiredYaw = 180.0*cos((i+90.0)*PI/180.0);
#endif


            //Initialize the plots you want to see
            UpdatePlot(CUR_DEPTH, currentDepth);
            UpdatePlot(SET_DEPTH, desiredDepth);
            UpdatePlot(CUR_ROLL, currentRoll);
            UpdatePlot(SET_ROLL, desiredDepth);
            UpdatePlot(CUR_PITCH, currentPitch);
            UpdatePlot(SET_PITCH, desiredPitch);
            UpdatePlot(CUR_YAW, currentYaw);
            UpdatePlot(SET_YAW, desiredYaw);
            //Incriment the number of points in the buffer
            numPlotPoints++;

            i+=0.1;

            XGetWindowAttributes(dpy, win, &gwa);
            //glViewport(0, 0, gwa.width, gwa.height);
            glViewport(0,0, WINDOW_X, WINDOW_Y);
            Render();
            glXSwapBuffers(dpy, win);

        }
}







void DrawDepthGuage()
{
    //Locals
    int i;

    float depth;

    char buffer[255];

    sprintf(buffer, "%.2f", currentDepth);

    depth = (currentDepth/DEPTH_METER_MAX)*((WINDOW_Y-WINDOW_Y/DEPTH_SKY)-(WINDOW_Y/2+WINDOW_Y/DEPTH_GND));

    //(WINDOW_Y-WINDOW_Y/DEPTH_SKY)-(WINDOW_Y/2+WINDOW_Y/DEPTH_GND)-(currentDepth/DEPTH_METER_MAX)*((WINDOW_Y-WINDOW_Y/DEPTH_SKY)-(WINDOW_Y/2+WINDOW_Y/DEPTH_GND));

    //Depth Guage
    glColor3f(0.8f , 0.8f, 1.0f );
    glBegin(GL_TRIANGLES);
    glVertex3f( WINDOW_X/3 , WINDOW_Y , 0 );
    glVertex3f( WINDOW_X/3 , WINDOW_Y-(WINDOW_Y/DEPTH_SKY) , 0 );
    glVertex3f( WINDOW_X/3*2 , WINDOW_Y-(WINDOW_Y/DEPTH_SKY) , 0 );

    glVertex3f( WINDOW_X/3 , WINDOW_Y , 0 );
    glVertex3f( WINDOW_X/3*2 , WINDOW_Y , 0 );
    glVertex3f( WINDOW_X/3*2 , WINDOW_Y-(WINDOW_Y/DEPTH_SKY) , 0 );


    glColor3f(0.0f, 0.5f, 1.0f);
    glVertex3f( WINDOW_X/3 , WINDOW_Y-(WINDOW_Y/DEPTH_SKY) , 0 );
    glColor3f(0.0f, 0.0f, 0.5f);
    glVertex3f( WINDOW_X/3 , WINDOW_Y-(WINDOW_Y/DEPTH_SKY) -((WINDOW_Y/2)-(WINDOW_Y/DEPTH_SKY)-(WINDOW_Y/DEPTH_GND)), 0 );
    glVertex3f( WINDOW_X/3*2 , WINDOW_Y-(WINDOW_Y/DEPTH_SKY)-((WINDOW_Y/2)-(WINDOW_Y/DEPTH_SKY)-(WINDOW_Y/DEPTH_GND)) , 0 );


    glColor3f(0.0f, 0.5f, 1.0f);
    glVertex3f( WINDOW_X/3 , WINDOW_Y-(WINDOW_Y/DEPTH_SKY) , 0 );
    glVertex3f( WINDOW_X/3*2 , WINDOW_Y-(WINDOW_Y/DEPTH_SKY), 0 );
    glColor3f(0.0f, 0.0f, 0.5f);
    glVertex3f( WINDOW_X/3*2 , WINDOW_Y-(WINDOW_Y/DEPTH_SKY)-((WINDOW_Y/2)-(WINDOW_Y/DEPTH_SKY)-(WINDOW_Y/DEPTH_GND)) , 0 );


    glColor3f(0.3f, 0.3, 0.3f);

    glVertex3f( WINDOW_X/3 , WINDOW_Y/2+(WINDOW_Y/DEPTH_SKY) , 0 );
    glVertex3f( WINDOW_X/3 , WINDOW_Y/2 , 0 );
    glVertex3f( WINDOW_X/3*2 , WINDOW_Y/2 , 0 );

    glVertex3f( WINDOW_X/3 , WINDOW_Y/2+(WINDOW_Y/DEPTH_SKY) , 0 );
    glVertex3f( WINDOW_X/3*2 , WINDOW_Y/2+(WINDOW_Y/DEPTH_SKY) , 0 );
    glVertex3f( WINDOW_X/3*2 , WINDOW_Y/2 , 0 );


    //Yard stick...thing

    glColor3f(DEPTH_METER_TOP_COLOR);
    glVertex3f( WINDOW_X/3 + ((WINDOW_X/DEPTH_SLDR_WIDTH)/4) , WINDOW_Y - (WINDOW_Y/DEPTH_SKY)/2 , 5 );

    glColor3f(DEPTH_METER_BOTTOM_COLOR);
    glVertex3f( WINDOW_X/3 + ((WINDOW_X/DEPTH_SLDR_WIDTH)/4) , WINDOW_Y/2 + (WINDOW_Y/DEPTH_GND) , 5 );
    glVertex3f( WINDOW_X/3 + ((WINDOW_X/DEPTH_SLDR_WIDTH/4)*2) , WINDOW_Y/2 + (WINDOW_Y/DEPTH_GND) , 5 );

    glColor3f(DEPTH_METER_TOP_COLOR);
    glVertex3f( WINDOW_X/3 + ((WINDOW_X/DEPTH_SLDR_WIDTH)/4) ,  WINDOW_Y - (WINDOW_Y/DEPTH_SKY)/2 , 5 );
    glVertex3f( WINDOW_X/3 + (((WINDOW_X/DEPTH_SLDR_WIDTH)/4)*2) , WINDOW_Y - (WINDOW_Y/DEPTH_SKY)/2 , 5 );

    glColor3f(DEPTH_METER_BOTTOM_COLOR);
    glVertex3f( WINDOW_X/3 + (((WINDOW_X/DEPTH_SLDR_WIDTH)/4)*2)  , WINDOW_Y/2 + (WINDOW_Y/DEPTH_GND), 5 );


    //Moving slider

    glColor3f(1.0f, 1.0f, 1.0f);

    glVertex3f( WINDOW_X/3 + (WINDOW_X/DEPTH_SLDR_OFST) , WINDOW_Y-(WINDOW_Y/DEPTH_SKY)-depth + (WINDOW_Y/DEPTH_SLDR_HEIGHT)/2, 5);
    glVertex3f( WINDOW_X/3 + (WINDOW_X/DEPTH_SLDR_OFST) , WINDOW_Y-(WINDOW_Y/DEPTH_SKY)-depth - (WINDOW_Y/DEPTH_SLDR_HEIGHT)/2, 5);
    glVertex3f( WINDOW_X/3 + (WINDOW_X/DEPTH_SLDR_OFST) + (WINDOW_X/DEPTH_SLDR_WIDTH) , WINDOW_Y-(WINDOW_Y/DEPTH_SKY) -depth - (WINDOW_Y/DEPTH_SLDR_HEIGHT)/2, 5);

    glVertex3f( WINDOW_X/3 + (WINDOW_X/DEPTH_SLDR_OFST) , WINDOW_Y-(WINDOW_Y/DEPTH_SKY)-depth + (WINDOW_Y/DEPTH_SLDR_HEIGHT)/2, 5);
    glVertex3f( WINDOW_X/3 + (WINDOW_X/DEPTH_SLDR_OFST) + (WINDOW_X/DEPTH_SLDR_WIDTH) , WINDOW_Y-(WINDOW_Y/DEPTH_SKY)-depth + (WINDOW_Y/DEPTH_SLDR_HEIGHT)/2, 5);
    glVertex3f( WINDOW_X/3 + (WINDOW_X/DEPTH_SLDR_OFST) + (WINDOW_X/DEPTH_SLDR_WIDTH) , WINDOW_Y-(WINDOW_Y/DEPTH_SKY)-depth - (WINDOW_Y/DEPTH_SLDR_HEIGHT)/2, 5);


    glEnd();



    //Graduate the depth meter
    glBegin(GL_LINES);

    glColor3f(1.0f, 1.0f, 1.0f);

    for(i=0; i<9; i++)
        {
            glVertex3f( WINDOW_X/3 + (WINDOW_X/DEPTH_SLDR_WIDTH)/4 , WINDOW_Y - (WINDOW_Y/DEPTH_SKY) - i*(((WINDOW_Y-(WINDOW_Y/DEPTH_SKY)) - (WINDOW_Y/2)+(WINDOW_Y/DEPTH_GND))/10) ,10.0f);
            glVertex3f( WINDOW_X/3 + ((WINDOW_X/DEPTH_SLDR_WIDTH)/4)*2, WINDOW_Y - (WINDOW_Y/DEPTH_SKY) - i*(((WINDOW_Y-(WINDOW_Y/DEPTH_SKY)) - (WINDOW_Y/2)+(WINDOW_Y/DEPTH_GND))/10) ,10.0f);
        }
    glEnd();



    //Draw red arrow from textbox to depth meter
    glBegin(GL_LINES);

    glColor3f(1.0f, 0.0f, 0.0f);

    //Top wing
    glVertex3f(WINDOW_X/3 + (WINDOW_X/DEPTH_SLDR_WIDTH)/2, WINDOW_Y - (WINDOW_Y/DEPTH_SKY)-depth, 15.0f);
    glVertex3f(WINDOW_X/3 + (WINDOW_X/DEPTH_SLDR_OFST)/2 , WINDOW_Y - (WINDOW_Y/DEPTH_SKY)/2-depth, 15.0f);

    //Bottom wing
    glVertex3f(WINDOW_X/3 + (WINDOW_X/DEPTH_SLDR_WIDTH)/2, WINDOW_Y - (WINDOW_Y/DEPTH_SKY)-depth, 15.0f);
    glVertex3f(WINDOW_X/3 + (WINDOW_X/DEPTH_SLDR_OFST)/2 , WINDOW_Y - ((WINDOW_Y/DEPTH_SKY)/2)*3-depth, 15.0f);

    //Arrow shaft
    glVertex3f(WINDOW_X/3 + (WINDOW_X/DEPTH_SLDR_WIDTH)/2, WINDOW_Y - (WINDOW_Y/DEPTH_SKY)-depth , 15.0f );
    glVertex3f(WINDOW_X/3 + (WINDOW_X/DEPTH_SLDR_OFST) , WINDOW_Y - (WINDOW_Y/DEPTH_SKY)-depth, 15.0f );
    glEnd();

    //Output text
    Text(buffer, WINDOW_X/3 + (WINDOW_X/DEPTH_SLDR_OFST) + (WINDOW_X/DEPTH_SLDR_OFST)/20, WINDOW_Y - (WINDOW_Y/DEPTH_SKY)-depth-(WINDOW_Y/DEPTH_SLDR_HEIGHT)/2 + (WINDOW_Y/DEPTH_SLDR_HEIGHT)/10, 1, 5, 0.0f,0.0f,0.0f );

    Text(buffer, WINDOW_X/3 + (WINDOW_X/DEPTH_SLDR_OFST), WINDOW_Y/2  + (WINDOW_Y/DEPTH_SLDR_HEIGHT)/10,2 , 5, 0.0f,1.0f,0.0f);


    return;

}







void DrawLevelGuage()
{
    //Locals
    int i;

    char buffer[255];

    //Draw the horizion
    glColor3f(0.0f, 0.0f, 1.0f);


    glBegin(GL_TRIANGLES);
    glVertex3f( LEVEL_METER_LEFT + LEVEL_METER_RADIUS, (currentPitch/50.0)*(LEVEL_METER_RADIUS) + LEVEL_METER_CENTER_Y, 0.0f);
    glVertex3f( LEVEL_METER_LEFT + LEVEL_METER_RADIUS + LEVEL_METER_RADIUS, LEVEL_METER_CENTER_Y + (currentPitch/50.0)*(LEVEL_METER_RADIUS) +  ((LEVEL_METER_RADIUS/2.0)*sin(currentRoll*PI/180.0)), 0.0f);
    glVertex3f( LEVEL_METER_LEFT + LEVEL_METER_RADIUS*2.0, LEVEL_METER_CENTER_Y - LEVEL_METER_RADIUS, 0.0f);

    glVertex3f( LEVEL_METER_LEFT + LEVEL_METER_RADIUS, LEVEL_METER_CENTER_Y + (currentPitch/50.0)*(LEVEL_METER_RADIUS), 0.0f);
    glVertex3f( LEVEL_METER_LEFT + LEVEL_METER_RADIUS/2.0 -LEVEL_METER_RADIUS/2.0, LEVEL_METER_CENTER_Y + (currentPitch/50.0)*(LEVEL_METER_RADIUS) - (LEVEL_METER_RADIUS/2.0)*sin(currentRoll*PI/180.0), 0.0f);
    glVertex3f( LEVEL_METER_LEFT, LEVEL_METER_CENTER_Y - LEVEL_METER_RADIUS, 0.0f);

    glVertex3f( LEVEL_METER_LEFT + LEVEL_METER_RADIUS, (currentPitch/50.0)*(LEVEL_METER_RADIUS) + LEVEL_METER_CENTER_Y, 0.0f);
    glVertex3f( LEVEL_METER_LEFT + LEVEL_METER_RADIUS*2.0, LEVEL_METER_CENTER_Y - LEVEL_METER_RADIUS, 0.0f);
    glVertex3f( LEVEL_METER_LEFT, LEVEL_METER_CENTER_Y - LEVEL_METER_RADIUS, 0.0f);

    glEnd();


    //Change drawing color
    glColor3f(0.0f, 1.0f, 0.0f);

    //Draw the level guage
    glBegin(GL_LINES);
    for( i=0 ; i<360 ; i++ )
        {
            glColor3f(0.0f, 1.0f, 0.0f);

            glVertex3f( LEVEL_METER_LEFT + LEVEL_METER_RADIUS + LEVEL_METER_RADIUS*cos((float)i*PI/180.0) , LEVEL_METER_CENTER_Y + LEVEL_METER_RADIUS*sin((float)i*PI/180.0) , 5.0 );
            glVertex3f( LEVEL_METER_LEFT + LEVEL_METER_RADIUS + LEVEL_METER_RADIUS*cos((float)(i+1)*PI/180.0) , LEVEL_METER_CENTER_Y + LEVEL_METER_RADIUS*sin((float)(i+1)*PI/180.0) , 5.0 );

            /*Clear the "water" from outside the level guage
              glColor3f(0.0f, 0.0f, 0.0f);
              if(i<90 || i>270)
              {
              glVertex3f( LEVEL_METER_LEFT + LEVEL_METER_RADIUS + LEVEL_METER_RADIUS*cos((float)i*PI/180.0) , LEVEL_METER_CENTER_Y +(int)( LEVEL_METER_RADIUS*sin((float)(i+1)*PI/180.0) ), 5.0 );
              glVertex3f( WINDOW_X , LEVEL_METER_CENTER_Y + (int)( LEVEL_METER_RADIUS*sin((float)i*PI/180.0) ), 15.0 );

              glVertex3f( LEVEL_METER_LEFT + LEVEL_METER_RADIUS + (int)( LEVEL_METER_RADIUS*cos((float)(i+1)*PI/180.0) ), LEVEL_METER_CENTER_Y + LEVEL_METER_RADIUS*sin((float)(i+1)*PI/180.0) , 5.0 );
              glVertex3f( WINDOW_X , LEVEL_METER_CENTER_Y + (int)( LEVEL_METER_RADIUS*sin((float)(i+1)*PI/180.0) ), 15.0 );


              }*/

        }

    glEnd();


    glColor3f(1.0f, 1.0f, 1.0f);


    //Draw the horizontal reference
    glColor3f(1.0f, 1.0f, 1.0f);
    glBegin(GL_LINES);

    glVertex3f( LEVEL_METER_LEFT, LEVEL_METER_CENTER_Y , 5.0f);
    glVertex3f( LEVEL_METER_LEFT + (LEVEL_METER_RADIUS*2.0)/3.0, LEVEL_METER_CENTER_Y, 5.0f);


    glVertex3f( LEVEL_METER_LEFT + (LEVEL_METER_RADIUS*2.0)/3.0, LEVEL_METER_CENTER_Y, 5.0f);
    glVertex3f( LEVEL_METER_LEFT + (LEVEL_METER_RADIUS*2.0)/3.0 + ((LEVEL_METER_RADIUS*2.0)/3.0)/4.0, LEVEL_METER_CENTER_Y - LEVEL_METER_RADIUS/5.0 , 5.0f);


    glVertex3f( LEVEL_METER_LEFT + (LEVEL_METER_RADIUS*2.0)/3.0 + ((LEVEL_METER_RADIUS*2.0)/3.0)/4.0, LEVEL_METER_CENTER_Y - LEVEL_METER_RADIUS/5.0 , 5.0f);
    glVertex3f( LEVEL_METER_LEFT + (LEVEL_METER_RADIUS*2.0)/3.0 + ((LEVEL_METER_RADIUS*2.0)/3.0)/2.0, LEVEL_METER_CENTER_Y , 5.0f);


    glVertex3f( LEVEL_METER_LEFT + (LEVEL_METER_RADIUS*2.0)/3.0 + ((LEVEL_METER_RADIUS*2.0)/3.0)/2.0, LEVEL_METER_CENTER_Y , 5.0f);
    glVertex3f( LEVEL_METER_LEFT + (LEVEL_METER_RADIUS*2.0)/3.0 +(((LEVEL_METER_RADIUS*2.0)/3.0)/4.0)*3.0, LEVEL_METER_CENTER_Y - LEVEL_METER_RADIUS/5.0 , 5.0f);

    glVertex3f( LEVEL_METER_LEFT + (LEVEL_METER_RADIUS*2.0)/3.0 +(((LEVEL_METER_RADIUS*2.0)/3.0)/4.0)*3.0, LEVEL_METER_CENTER_Y - LEVEL_METER_RADIUS/5.0 , 5.0f);
    glVertex3f( LEVEL_METER_LEFT + (LEVEL_METER_RADIUS*2.0)/3.0 + ((LEVEL_METER_RADIUS*2.0)/3.0), LEVEL_METER_CENTER_Y , 5.0f);


    glVertex3f( LEVEL_METER_LEFT + (LEVEL_METER_RADIUS*2.0)/3.0 + ((LEVEL_METER_RADIUS*2.0)/3.0), LEVEL_METER_CENTER_Y , 5.0f);
    glVertex3f( LEVEL_METER_LEFT + (LEVEL_METER_RADIUS*2.0), LEVEL_METER_CENTER_Y , 5.0f);

    glEnd();


    //Graduate the level
    glColor3f( 1.0f, 1.0f, 1.0f);

    glBegin(GL_LINES);

    for(i=1; i<10; i++)
        {
            glVertex3f( LEVEL_METER_LEFT + LEVEL_METER_RADIUS - LEVEL_METER_RADIUS/5.0, LEVEL_METER_CENTER_Y - LEVEL_METER_RADIUS + ((float)i/10.0)*(LEVEL_METER_RADIUS*2.0), 10.0f);
            glVertex3f( LEVEL_METER_LEFT + LEVEL_METER_RADIUS + LEVEL_METER_RADIUS/5.0, LEVEL_METER_CENTER_Y - LEVEL_METER_RADIUS + ((float)i/10.0)*(LEVEL_METER_RADIUS*2.0), 10.0f);

        }

    glEnd();

    for(i=1; i<10; i++)
        {
            sprintf(buffer, "%d", 10*abs(5-i));

            Text(buffer, LEVEL_METER_LEFT + LEVEL_METER_RADIUS - LEVEL_METER_RADIUS/4 + LEVEL_METER_RADIUS/15, LEVEL_METER_CENTER_Y - LEVEL_METER_RADIUS + ((float)i/10.0)*(LEVEL_METER_RADIUS*2) , 1, 0 , 1.0f, 0.0f, 0.0f);

        }



    return;
}







void Text(char* str, int x, int y, int size, int width, float red, float green, float blue)
{
    //Locals
    int i,strLength;

    float X1, Y1, scale;

    int current_number;

    //Find the length of the input string
    strLength = strlen(str);

    //Setup the text string from the arguments
    scale=(float)size/20.0;
    scale=(float)scale*(WINDOW_X/640);
    X1 = (float)x;
    Y1 = (float)y;

    //Right justify the output if a non-zero width was given
    X1 += ((175.0 + 75.0)*scale)*(width-strLength);

    glColor3f(red, green, blue);

    //Draw 7-segment LED-style display
    glBegin(GL_TRIANGLES);

    for(i=0; i<strLength; i++)
        {

            if(str[i]!='.' && str[i]!='-')
                current_number = (int)str[i]-0x30;
            else
                current_number = (int)str[i];


            if((char)current_number == '.')
                {
                    //Draw decimal point
                    glVertex3f(X1 + 0.0f*scale, Y1+0.0f*scale, 10.0f);
                    glVertex3f(X1 + 50.0f*scale, Y1+0.0f*scale, 10.0f);
                    glVertex3f(X1 + 50.0f*scale, Y1+50.0f*scale, 10.0f);

                    glVertex3f(X1 + 50.0f*scale, Y1+50.0f*scale, 10.0f);
                    glVertex3f(X1 + 0.0f*scale, Y1+50.0f*scale, 10.0f);
                    glVertex3f(X1 + 0.0f*scale, Y1+0.0f*scale, 10.0f);
                }


            if(current_number==2 || current_number==3 || current_number==5 || current_number==6 || current_number==7 || current_number==8 || current_number==9 || current_number==0)
                {
                    //top segment
                    glVertex3f(X1 + 0.0f*scale, Y1 + scale*200.0f, 10.0f );
                    glVertex3f(X1 + 175.0f*scale, Y1 + scale*200.0f, 10.0f );
                    glVertex3f(X1 + 25.0f*scale, Y1 + scale*175.0f, 10.0f );

                    glVertex3f(X1 + 175.0f*scale, Y1 + scale*200.0f, 10.0f );
                    glVertex3f(X1 + 150.0f*scale, Y1 + scale*175.0f, 10.0f );
                    glVertex3f(X1 + 25.0f*scale, Y1 + scale*175.0f, 10.0f );
                }

            if(current_number=='-' || current_number==2 || current_number==3 || current_number==4 ||current_number==5 || current_number==6 || current_number==8 || current_number==9)
                {
                    //middle segment
                    glVertex3f(X1 + 0.0f*scale, Y1 + scale*100.0f, 10.0f );
                    glVertex3f(X1 + 175.0f*scale, Y1 + scale*100.0f, 10.0f );
                    glVertex3f(X1 + 25.0f*scale, Y1 + scale*112.5f, 10.0f );

                    glVertex3f(X1 + 25.0f*scale, Y1 + scale*112.5f, 10.0f );
                    glVertex3f(X1 + 175.0f*scale, Y1 + scale*100.0f, 10.0f );
                    glVertex3f(X1 + 150.0f*scale, Y1 + scale*112.5f, 10.0f );

                    glVertex3f(X1 + 0.0f*scale, Y1 + scale*100.0f, 10.0f );
                    glVertex3f(X1 + 175.0f*scale, Y1 + scale*100.0f, 10.0f );
                    glVertex3f(X1 + 25.0f*scale, Y1 + scale*87.5f, 10.0f );

                    glVertex3f(X1 + 25.0f*scale, Y1 + scale*87.5f, 10.0f );
                    glVertex3f(X1 + 175.0f*scale, Y1 + scale*100.0f, 10.0f );
                    glVertex3f(X1 + 150.0f*scale, Y1 + scale*87.5f, 10.0f );

                }

            if(current_number==2 || current_number==3 || current_number==5 || current_number==6 || current_number==8 || current_number==9 || current_number==0)
                {
                    //bottom segment
                    glVertex3f(X1 + 0.0f*scale, Y1 + scale*0.0f, 10.0f );
                    glVertex3f(X1 + 175.0f*scale, Y1 + scale*0.0f, 10.0f );
                    glVertex3f(X1 + 25.0f*scale, Y1 + scale*25.0f, 10.0f );

                    glVertex3f(X1 + 175.0f*scale, Y1 + scale*0.0f, 10.0f );
                    glVertex3f(X1 + 150.0f*scale, Y1 + scale*25.0f, 10.0f );
                    glVertex3f(X1 + 25.0f*scale, Y1 + scale*25.0f, 10.0f );
                }


            if(current_number==4 || current_number==5 || current_number==6 || current_number==8 || current_number==9 || current_number==0)
                {
                    //top-left segment
                    glVertex3f(X1 + 0.0f*scale, Y1 + scale*200.0f, 10.0f );
                    glVertex3f(X1 + 0.0f*scale, Y1 + scale*100.0f, 10.0f );
                    glVertex3f(X1 + 25.0f*scale, Y1 + scale*175.0f, 10.0f );

                    glVertex3f(X1 + 25.0f*scale, Y1 + scale*175.0f, 10.0f );
                    glVertex3f(X1 + 0.0f*scale, Y1 + scale*100.0f, 10.0f );
                    glVertex3f(X1 + 25.0f*scale, Y1 + scale*112.5f, 10.0f );
                }


            if(current_number==1 || current_number==2 || current_number==3 || current_number==4 || current_number==7 || current_number==8 || current_number==9 || current_number==0)
                {
                    //top-right segment
                    glVertex3f(X1 + 175.0f*scale, Y1 + scale*200.0f, 10.0f );
                    glVertex3f(X1 + 150.0f*scale, Y1 + scale*175.0f, 10.0f );
                    glVertex3f(X1 + 175.0f*scale, Y1 + scale*100.0f, 10.0f );

                    glVertex3f(X1 + 150.0f*scale, Y1 + scale*175.0f, 10.0f );
                    glVertex3f(X1 + 175.0f*scale, Y1 + scale*100.0f, 10.0f );
                    glVertex3f(X1 + 150.0f*scale, Y1 + scale*112.5f, 10.0f );
                }


            if(current_number==2 || current_number==6 || current_number==8 || current_number==0)
                {

                    //bottom-left segment
                    glVertex3f(X1 + 0.0f*scale, Y1 + scale*100.0f, 10.0f );
                    glVertex3f(X1 + 0.0f*scale, Y1 + scale*0.0f, 10.0f );
                    glVertex3f(X1 + 25.0f*scale, Y1 + scale*87.5f, 10.0f );

                    glVertex3f(X1 + 25.0f*scale, Y1 + scale*87.5f, 10.0f );
                    glVertex3f(X1 + 0.0f*scale, Y1 + scale*0.0f, 10.0f );
                    glVertex3f(X1 + 25.0f*scale, Y1 + scale*25.0f, 10.0f );

                }


            if(current_number==1 || current_number==3 || current_number==4 || current_number==5 || current_number==6 || current_number==7 || current_number==8 || current_number==9 || current_number==0)
                {


                    //bottom-right segment
                    glVertex3f(X1 + 175.0f*scale, Y1 + scale*100.0f, 10.0f );
                    glVertex3f(X1 + 150.0f*scale, Y1 + scale*87.5f, 10.0f );
                    glVertex3f(X1 + 175.0f*scale, Y1 + scale*0.0f, 10.0f );

                    glVertex3f(X1 + 150.0f*scale, Y1 + scale*87.5f, 10.0f );
                    glVertex3f(X1 + 175.0f*scale, Y1 + scale*0.0f, 10.0f );
                    glVertex3f(X1 + 150.0f*scale, Y1 + scale*25.0f, 10.0f );
                }


            //Set the coordinates for the next number
            X1 += (175.0 + 75.0)*scale;
        }

    glEnd();

    return;
}

void UpdatePlot(int plotNum, float data)
{

    //Locals
    DATA_POINT* current;

    //If this is the first data point in the set
    if(plot[plotNum]==NULL)
        {
            //Allocate memory for the first datapoint
            plot[plotNum] = (DATA_POINT*)calloc(1, sizeof(DATA_POINT));

            //Set parameters
            plot[plotNum]->data = data;
            plot[plotNum]->next = NULL;

        }
    //Else, if this is not the first point int the set
    else
        {
            //Check to see if the data has reached the end of the screen
            if(numPlotPoints<((WINDOW_X/PLOT_RES))*2)
                {
                    //Allocate space for the new datapoint
                    current = (DATA_POINT*)calloc(1, sizeof(DATA_POINT));

                    //Set parameters
                    current->data = data;
                    current->next = plot[plotNum];

                    //Link this item to the list
                    plot[plotNum] = current;

                }
            else
                {
                    current = plot[plotNum];

                    //Set the "current" to point to the tail of the list (oldest value added)
                    while(current->next->next!=NULL)current = current->next;

                    //Free the oldest item in the linked list
                    free(current->next);

                    //Set the "next" pointer of the new end-of-list
                    current->next = NULL;

                    //Allocate space for the new datapoint
                    current = (DATA_POINT*)calloc(1, sizeof(DATA_POINT));

                    //Set parameters
                    current->data = data;
                    current->next = plot[plotNum];

                    //Link this item to the list
                    plot[plotNum] = current;

                    //printf("\nDeleted");
                    //fflush(NULL);
                }
        }


    return;
}




void DrawPlots()
{
    int i;
    float j;
    DATA_POINT* current;

    for(i=0; i<MAX_PLOTS; i++)
        {
            j=0;
            current = plot[i];

            switch(i)
                {
                case CUR_DEPTH:glColor3f(0.0f, 0.0f, 1.0f);
                    break;

                case SET_DEPTH: glColor3f(0.0f, 0.0f, 0.3f);
                    break;

                case CUR_ROLL:glColor3f(1.0f, 0.0f, 0.0F);
                    break;

                case SET_ROLL:glColor3f(0.3f, 0.0f, 0.0f);
                    break;

                case CUR_PITCH:glColor3f(0.0f, 1.0f, 0.0f);
                    break;

                case SET_PITCH:glColor3f(0.0f, 0.3f, 0.0f);
                    break;

                case CUR_YAW:glColor3f(1.0f, 0.5f, 0.0f);
                    break;

                case SET_YAW:glColor3f(0.3f, 0.15f, 0.0f);
                    break;
                }

            glBegin(GL_LINES);

            while(current!=NULL)
                {


                    if(i==CUR_DEPTH || i==SET_DEPTH)
                        {
                            glVertex3f(WINDOW_X-(j), WINDOW_Y/4.0 - (WINDOW_Y/4.0)*((current->data)/(DEPTH_METER_MAX)), 15.0f);

                            current=current->next;

                            if(current==NULL)
                                break;

                            glVertex3f(WINDOW_X-(j+PLOT_RES), WINDOW_Y/4.0 - (WINDOW_Y/4.0)*((current->data)/(DEPTH_METER_MAX)), 15.0f);
                        }
                    else if(i==CUR_ROLL || i==SET_ROLL || i==CUR_PITCH || i==SET_PITCH || i==CUR_YAW || i==SET_YAW)
                        {
                            glVertex3f(WINDOW_X-(j), WINDOW_Y/4.0 - (WINDOW_Y/4.0)*((current->data)/(180.0)), 15.0f);

                            current=current->next;

                            if(current==NULL)
                                break;

                            glVertex3f(WINDOW_X-(j+PLOT_RES), WINDOW_Y/4.0 - (WINDOW_Y/4.0)*((current->data)/(180.0)), 15.0f);


                        }

                    j+=PLOT_RES;

                    current = current->next;
                }

            glEnd();

        }

    return;

}
