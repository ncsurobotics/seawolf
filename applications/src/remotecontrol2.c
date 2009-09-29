
#include "seawolf.h"

#include <ncurses.h>
#include <pthread.h>
#include <math.h>

#define F_MAX 10             /* Adjust me! */
#define F_SET 3              /* Adjust me! */
#define DEPTH_STEP 0.25      /* Step size for depth */
#define SURFACE 0            /* Surface is 0 feet deep */
#define MAX_DEPTH 15         /* Maximum targeted depth */

#define SIGN(n) ((int) (((float)(n) == 0.0) ? 0 : (abs((float)(n)) / (n))))
#define F_SCALE ((float) (F_SET + F_MAX) / F_MAX)

static float depth_heading = SURFACE;
static bool running = true;

void* notify_monitor(void* _n) {
    char action[64], data[64];
    int aft = 0, portx = 0, porty = 0, starx = 0, stary = 0;
    float depth = 0;

    char* display = "    \n\
     Seawolf III         \n\
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

        Notify_get(action, data);

        if(strcmp(data, "Aft") == 0) {
            aft = (int) SeaSQL_getAft();
        } else if(strcmp(data, "PortY") == 0) {
            porty = (int) SeaSQL_getPortY();
        } else if(strcmp(data, "StarY") == 0) {
            stary = (int) SeaSQL_getStarY();
        } else if(strcmp(data, "PortX") == 0) {
            portx = (int) SeaSQL_getPortX();
        } else if(strcmp(data, "StarX") == 0) {
            starx = (int) SeaSQL_getStarX();
        } else if(strcmp(data, "Depth") == 0) {
            depth = SeaSQL_getDepth();
        }
    }

    return NULL;
}

void updateThrusters(int magnitude, int rotate) {
    float mag_f = (float) abs(magnitude);
    float rot_f = (float) abs(rotate);
    int mag_sign = SIGN(magnitude);
    int rot_sign = SIGN(rotate);
    float forward_scale = (F_SCALE * mag_f) / (F_SET + mag_f);
    float rotate_scale = (F_SCALE * rot_f) / (F_SET + rot_f);

    int port, star;
    port = mag_sign * THRUSTER_MAX * forward_scale;
    star = port;

    if(rot_sign > 0) {
        star *= (1 - rotate_scale);
    } else if(rot_sign < 0) {
        port *= (1 - rotate_scale);
    }

    Notify_send("THRUSTER_REQUEST", Util_format("Forward %d %d", (int)Util_inRange(-THRUSTER_MAX, star, THRUSTER_MAX), (int)Util_inRange(-THRUSTER_MAX, port, THRUSTER_MAX)));
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Remote control 2");

    int magnitude = 0, rotate = 0, c;

    initscr();
    cbreak();
    raw();
    noecho();
    keypad(stdscr, TRUE);

    pthread_t display_thread;
    pthread_create(&display_thread, NULL, notify_monitor, NULL);

    updateThrusters(0, 0);
    SeaSQL_setDepthHeading(depth_heading);

    while(running) {
        /* Copy key and clear. There is a race condition here but I don't care */
        c = getch();
    
        if(c == KEY_UP || c == 'w') {
            /* Increase speed */
            magnitude = Util_inRange(-F_MAX, magnitude + 1, F_MAX);
            updateThrusters(magnitude, rotate);

        } else if(c == KEY_DOWN || c == 's') {
            /* Decrease speed */
            magnitude = Util_inRange(-F_MAX, magnitude - 1, F_MAX);
            updateThrusters(magnitude, rotate);

        } else if(c == KEY_RIGHT || c == 'd') {
            /* Turn clockwise */
            rotate = Util_inRange(-F_MAX, rotate + 1, F_MAX);
            updateThrusters(magnitude, rotate);

        } else if(c == KEY_LEFT || c == 'a') {
            /* Turn counterclockwise */
            rotate = Util_inRange(-F_MAX, rotate - 1, F_MAX);
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
            SeaSQL_setDepthHeading(depth_heading);

        } else if(c == 'j') {
            /* Depth down (towards bottom) */
            depth_heading = Util_inRange(SURFACE, depth_heading - DEPTH_STEP, MAX_DEPTH);
            SeaSQL_setDepthHeading(depth_heading);

        } else if(c == 'q') {
            running = false;
            break;
        }
    }

    updateThrusters(0, 0);
    SeaSQL_setDepthHeading(SURFACE);

    endwin();
    Seawolf_close();
    return 0;
}
