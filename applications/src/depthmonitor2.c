
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
    float stern, port, star, bow, strafet, strafeb;
    float depth, depthheading, seapitch, searoll, seayaw;
    float yawheading, pitchheading, rollheading;
    float depthpaused, yawpaused, pitchpaused, rollpaused;

    char* display = "  \n\
        Seawolf III    \n\
                       \n\
   %10.2f/%.2f/%.1f \tDepth Heading/Depth/paused  \n\
                       \n\
   %10.2f/%.2f/%.f \tPitch Heading/Pitch/paused  \n\
                       \n\
   %10.2f/%.2f/%.1f \tRoll Heading/Roll/paused  \n\
                       \n\
   %10.2f/%.2f/%.1f \tYaw Heading/Yaw/paused  \n\
                       \n\
                       \n\
                       \n\
  Bow:       %7.2f      \n\
  Port:      %7.2f      \n\
  Star:      %7.2f      \n\
  Stern:     %7.2f      \n\
  StrafeT:   %7.2f      \n\
  StrafeB:   %7.2f      \n\
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

    Var_bind("StrafeT", &strafet);
    Var_bind("StrafeB", &strafeb);
    Var_bind("Stern", &stern);
    Var_bind("Bow", &bow);
    Var_bind("Port", &port);
    Var_bind("Star", &star);
    Var_bind("Depth", &depth);
    Var_bind("SEA.Pitch", &seapitch);
    Var_bind("SEA.Roll", &searoll);
    Var_bind("SEA.Yaw", &seayaw);
    Var_bind("DepthPID.Heading", &depthheading);
    Var_bind("YawPID.Heading", &yawheading);
    Var_bind("PitchPID.Heading", &pitchheading);
    Var_bind("RollPID.Heading", &rollheading);
    Var_bind("DepthPID.Paused", &depthpaused);
    Var_bind("YawPID.Paused", &yawpaused);
    Var_bind("RollPID.Paused", &rollpaused);
    Var_bind("PitchPID.Paused", &pitchpaused);
    
    while(quit == false) {
        clear();
        printw(display, depthheading, depth, depthpaused, pitchheading, seapitch, pitchpaused, rollheading, searoll, rollpaused, yawheading, seayaw, yawpaused, bow, port, star, stern, strafet, strafeb);
        refresh();

        Var_sync();
    }

    endwin();
    Seawolf_close();
    return 0;
}
