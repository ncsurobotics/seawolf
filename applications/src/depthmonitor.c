
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

static bool quit = false;

static int control_heading(void) {
    float depth_heading = 0;
    WINDOW* w = newwin(1, 1, 0, 0);
    int c;

    Var_set("DepthPID.Heading", depth_heading);
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
        Var_set("DepthPID.Heading", depth_heading);
    }

    quit = true;
    Var_set("DepthPID.Heading", 0);
    
    return 0;
}

int main(void) {
    float stern, port, star, bow, strafe;
    float depth, depthheading, seapitch, searoll, seayaw;

    char* display = "  \n\
        Seawolf III    \n\
                       \n\
   %10.2f/%.2f \tDepth Heading/Depth  \n\
                       \n\
   %10.2f %.2f \tPitch/Roll \n\
      %10.2f   \tYaw   \n\
                       \n\
                       \n\
         %7.2f         \n\
                       \n\
         %7.2f         \n\
  %7.2f       %7.2f      \n\
                       \n\
                       \n\
         %7.2f         \n\
";
    
    /* Init libseawolf */
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Remote control");

    /* Init curses */
    initscr();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);

    Task_background(control_heading);

    Var_bind("Strafe", &strafe);
    Var_bind("Stern", &stern);
    Var_bind("Bow", &bow);
    Var_bind("Port", &port);
    Var_bind("Star", &star);
    Var_bind("Depth", &depth);
    Var_bind("SEA.Pitch", &seapitch);
    Var_bind("SEA.Roll", &searoll);
    Var_bind("SEA.Yaw", &seayaw);
    Var_bind("Depth", &depth);
    Var_bind("DepthPID.Heading", &depthheading);
    
    while(quit == false) {
        clear();
        printw(display, depthheading, depth, seapitch, searoll, seayaw, bow, strafe, port, star, stern);
        refresh();

        Var_sync();
    }

    endwin();
    Seawolf_close();
    return 0;
}
