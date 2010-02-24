
#include "seawolf.h"

#include <ctype.h>
#include <stdio.h>
#include <ncurses.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>

#define MIN_SPEED (-60)
#define MAX_SPEED (60)
#define STEP (5)

#define ADJUST(x) Util_inRange(MIN_SPEED, (x), MAX_SPEED)

static float depth_heading = 0;
static bool quit = false;

static void* control_heading(void* _n) {
    int c;
    WINDOW* w = newwin(1, 1, 0, 0);
    Var_set("DepthHeading", depth_heading);
    while(true) {
        c = wgetch(w);
        if(c == 'q') {
            break;
        } else if(c == 'u') {
            depth_heading = Util_inRange(0, depth_heading + 0.25, 500);
        } else if(c == 'j') {
            depth_heading = Util_inRange(0, depth_heading - 0.25, 500);
        } else {
            continue;
        }
        Var_set("DepthHeading", depth_heading);
    }

    quit = true;
    Var_set("DepthHeading", 0);
    
    return NULL;
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Remote control");

    initscr();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);

    char* display = "    \n\
     Seawolf III         \n\
                         \n\
  %10.2f/%.2f            \n\
  %10.2f %.2f Pitch/Roll \n\
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

    int aft = 0, portx = 0, porty = 0, starx = 0, stary = 0;
    float depth=0, seapitch = 0, searoll = 0;
    char action[64], data[64];

    pthread_t control_thread;
    pthread_create(&control_thread, NULL, control_heading, NULL);

    /* Filter for our messages */
    Notify_filter(FILTER_MATCH, "UPDATED Aft");
    Notify_filter(FILTER_MATCH, "UPDATED PortY");
    Notify_filter(FILTER_MATCH, "UPDATED StarY");
    Notify_filter(FILTER_MATCH, "UPDATED PortX");
    Notify_filter(FILTER_MATCH, "UPDATED StarX");
    Notify_filter(FILTER_MATCH, "UPDATED Depth");
    Notify_filter(FILTER_MATCH, "UPDATED IMU");
    Notify_filter(FILTER_MATCH, "UPDATED DepthHeading");

    while(! quit) {
        clear();
        printw(display, depth_heading, depth, seapitch, searoll, porty, stary, portx, starx, aft);
        refresh();

        Notify_get(action, data);

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
        } else if(strcmp(data, "IMU") == 0) {
            seapitch = Var_get("SEA.Pitch");
            searoll = Var_get("SEA.Roll");
        }
    }

    endwin();
    Seawolf_close();
    return 0;
}
