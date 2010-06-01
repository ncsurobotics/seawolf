
#include "seawolf.h"
#include "seawolf3.h"

#include <ncurses.h>
#include <pthread.h>
#include <math.h>

#define SIGN(n) (((n) < 0) ? (-1) : (((n) > 0) ? 1 : 0))

/* Don't change these */
#define F_MAX 1.0
#define R_MAX 1.0
#define F_INC 0.1
#define R_INC 0.1

/* The forward momentum and rotation are raised to these powers respectively */
#define F_POWER_FACTOR 0.8
#define R_POWER_FACTOR 1.3

/* Maximum proportion of power devoted to rotation (80%) */
#define R_FRAC_MAX 0.8

/* Step size for depth */
#define DEPTH_STEP 0.25

/* Surface is 0 feet deep */
#define SURFACE 0

/* Maximum targeted depth */
#define MAX_DEPTH 15

static bool running = true;
static float depth_heading = SURFACE;

static void* notify_monitor(void* _n) {
    char data[64];
    int aft = 0, portx = 0, porty = 0, starx = 0, stary = 0;
    float depth = 0;

    char* display = "    \n\
     Remote Controll     \n\
                         \n\
  %10.2f/%.2f            \n\
                         \n\
                         \n\
        %-6d %4d         \n\
                         \n\
                         \n\
    %-7d     %7d         \n\
                         \n\
                         \n\
                         \n\
    %10d                 \n\
";

    Notify_filter(FILTER_MATCH, "UPDATED Aft");
    Notify_filter(FILTER_MATCH, "UPDATED PortY");
    Notify_filter(FILTER_MATCH, "UPDATED StarY");
    Notify_filter(FILTER_MATCH, "UPDATED PortX");
    Notify_filter(FILTER_MATCH, "UPDATED StarX");
    Notify_filter(FILTER_MATCH, "UPDATED Depth");
    Notify_filter(FILTER_MATCH, "UPDATED DepthHeading");

    while(running) {
        clear();
        printw(display, depth_heading, depth, porty, stary, portx, starx, aft);
        refresh();

        Notify_get(NULL, data);

        if(strcmp(data, "Aft") == 0) {
            aft = (int) Var_get("Aft");
        } else if(strcmp(data, "PortY") == 0) {
            porty = (int) Var_get("PortY");
        } else if(strcmp(data, "StarY") == 0) {
            stary = (int) Var_get("StarY");
        } else if(strcmp(data, "PortX") == 0) {
            portx = (int) Var_get("PortX");
        } else if(strcmp(data, "StarX") == 0) {
            starx = (int) Var_get("StarX");
        } else if(strcmp(data, "Depth") == 0) {
            depth = Var_get("Depth");
        }
    }

    return NULL;
}

static void updateThrusters(float magnitude, float rotate) {
    float mag_f = fabs(magnitude);
    float rot_f = fabs(rotate);
    int mag_sign = SIGN(magnitude);
    int rot_sign = SIGN(rotate);
    int offset;
    int port, star;

    /* Bend power curves for better control */
    mag_f = pow(mag_f, F_POWER_FACTOR);
    rot_f = pow(rot_f, R_POWER_FACTOR);

    /* Calculate rotational offset */
    offset = (int)(rot_f * R_FRAC_MAX * THRUSTER_MAX);
    star = port = (int) (mag_f * mag_sign * (THRUSTER_MAX-offset));

    /* Add in offset with correct sign */
    star += offset * rot_sign;
    port -= offset * rot_sign;

    /* Bound for good measure */
    star = Util_inRange(-THRUSTER_MAX, star, THRUSTER_MAX);
    port = Util_inRange(-THRUSTER_MAX, port, THRUSTER_MAX);

    /* Send out */
    Notify_send("THRUSTER_REQUEST", Util_format("Forward %d %d", (int)star, (int)port));
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Remote control");

    int c;
    float magnitude = 0, rotate = 0;

    initscr();
    cbreak();
    raw();
    noecho();
    keypad(stdscr, TRUE);

    pthread_t display_thread;
    pthread_create(&display_thread, NULL, notify_monitor, NULL);

    updateThrusters(0, 0);
    Var_set("DepthHeading", depth_heading);

    while(running) {
        /* Copy key and clear. There is a race condition here but I don't care */
        c = getch();
    
        if(c == KEY_UP || c == 'w') {
            /* Increase speed */
            magnitude = Util_inRange(-F_MAX, magnitude + F_INC, F_MAX);
            updateThrusters(magnitude, rotate);

        } else if(c == KEY_DOWN || c == 's') {
            /* Decrease speed */
            magnitude = Util_inRange(-F_MAX, magnitude - F_INC, F_MAX);
            updateThrusters(magnitude, rotate);

        } else if(c == KEY_RIGHT || c == 'd') {
            /* Turn clockwise */
            rotate = Util_inRange(-R_MAX, rotate + R_INC, R_MAX);
            updateThrusters(magnitude, rotate);

        } else if(c == KEY_LEFT || c == 'a') {
            /* Turn counterclockwise */
            rotate = Util_inRange(-R_MAX, rotate - R_INC, R_MAX);
            updateThrusters(magnitude, rotate);
           
        } else if(c == '0') {
            /* Reset xy motion */
            magnitude = 0;
            rotate = 0;
            updateThrusters(magnitude, rotate);

        } else if(c == 'h') {
            /* Reset heading */
            rotate = 0;
            updateThrusters(magnitude, rotate);

        } else if(c == 'u') {
            /* Depth up (towards surface) */
            depth_heading = Util_inRange(SURFACE, depth_heading + DEPTH_STEP, MAX_DEPTH);
            Var_set("DepthHeading", depth_heading);

        } else if(c == 'j') {
            /* Depth down (towards bottom) */
            depth_heading = Util_inRange(SURFACE, depth_heading - DEPTH_STEP, MAX_DEPTH);
            Var_set("DepthHeading", depth_heading);

        } else if(c == 'q') {
            running = false;
            break;
        }
    }

    updateThrusters(0, 0);
    Var_set("DepthHeading", SURFACE);

    endwin();
    Seawolf_close();
    return 0;
}
