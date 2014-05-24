
#include "seawolf.h"

#include <ctype.h>
#include <stdio.h>
#include <ncurses.h>

#define MIN_SPEED (-1.0)
#define MAX_SPEED (1.0)
#define STEP (0.05)

#define ADJUST(x) Util_inRange(MIN_SPEED, (x), MAX_SPEED)

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Thruster Controller");

    initscr();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);

    int c;
    char* display = "   \n\
  Thruster Controller   \n\
                        \n\
  Bow:       %3.2f      \n\
  Port:      %3.2f      \n\
  Star:      %3.2f      \n\
  Stern:     %3.2f      \n\
  StrafeT:   %3.2f      \n\
  StrafeB:   %3.2f      \n\
";

    float bow=0.0, stern=0.0, port=0.0, star=0.0, strafet=0.0, strafeb=0.0;
    int addsub = 1;
        
    /* Turn off drivers */
    Var_set("Port", 0.0);
    Var_set("Star", 0.0);
    Var_set("Bow", 0.0);
    Var_set("Stern", 0.0);
    Var_set("StrafeT", 0.0);
    Var_set("StrafeB", 0.0);
    
    while(true) {
        printw(display, bow, port, star, stern, strafet, strafeb);
        refresh();

        c = getch();
        clear();

        addsub = -1;
        if(isupper(c)) {
            addsub = 1;
        }
        c = tolower(c);

        switch(c) {
        case 'w':
            bow = ADJUST(bow + (addsub * STEP));
            Var_set("Bow", bow);
            break;

        case 's':
            stern = ADJUST(stern + (addsub * STEP));
            Var_set("Stern", stern);
            break;

        case 'a':
            port = ADJUST(port + (addsub * STEP));
            Var_set("Port", port);
            break;

        case 'd':
            star = ADJUST(star + (addsub * STEP));
            Var_set("Star", star);
            break;

        case 'z':
            strafet = ADJUST(strafet + (addsub * STEP));
            Var_set("StrafeT", strafet);
            break;

        case 'x':
            strafeb = ADJUST(strafeb + (addsub * STEP));
            Var_set("StrafeB", strafeb);
            break;
        }

        if(c == 'q') {
            break;
        }
    }

    endwin();

    /* Turn off drivers */
    Var_set("Port", 0);
    Var_set("Star", 0);
    Var_set("Bow", 0);
    Var_set("Stern", 0);
    Var_set("StrafeT", 0);
    Var_set("StrafeB", 0);

    Seawolf_close();
    return 0;
}
