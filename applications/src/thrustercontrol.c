
#include "seawolf.h"

#include <ctype.h>
#include <stdio.h>
#include <ncurses.h>

#define MIN_SPEED (-60)
#define MAX_SPEED (60)
#define STEP (5)

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
        %-6d %4d        \n\
                        \n\
                        \n\
    %-7d     %7d        \n\
                        \n\
                        \n\
                        \n\
    %10d                \n\
";

    int aft = 0, portx = 0, porty = 0, starx = 0, stary = 0;
    int addsub = 1;
        
    /* Turn off drivers */
    Var_set("PortX", 0);
    Var_set("PortY", 0);
    Var_set("StarX", 0);
    Var_set("StarY", 0);
    Var_set("Aft", 0);

    while(1) {
        printw(display, porty, stary, portx, starx, aft);
        refresh();
        c = getch();
        clear();

        addsub = -1;
        if(isupper(c)) {
            addsub = 1;
        }
        c = tolower(c);

        switch(c) {
        case 'u':
            porty = ADJUST(porty + (addsub * STEP));
            Var_set("PortY", porty);
            break;
        case 'j':
            portx = ADJUST(portx + (addsub * STEP));
            Var_set("PortX", portx);
            break;
        case 'o':
            stary = ADJUST(stary + (addsub * STEP));
            Var_set("StarY", stary);
            break;
        case 'l':
            starx = ADJUST(starx + (addsub * STEP));
            Var_set("StarX", starx);
            break;
        case 'k':
            aft = ADJUST(aft + (addsub * STEP));
            Var_set("Aft", aft);
            break;
        }

        if(c == 'q') {
            break;
        }
    }

    /* Turn off drivers */
    Var_set("PortX", 0);
    Var_set("PortY", 0);
    Var_set("StarX", 0);
    Var_set("StarY", 0);
    Var_set("Aft", 0);

    Seawolf_close();
    endwin();
    return 0;
}
