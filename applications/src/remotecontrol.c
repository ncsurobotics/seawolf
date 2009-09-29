
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
    Seawolf_init("Remote control");

    initscr();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);

    int c;
    char* display = "   \n\
     Seawolf III        \n\
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
    SeaSQL_setPortX(0);
    SeaSQL_setPortY(0);
    SeaSQL_setStarX(0);
    SeaSQL_setStarY(0);
    SeaSQL_setAft(0);

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
            SeaSQL_setPortY(porty);
            break;
        case 'j':
            portx = ADJUST(portx + (addsub * STEP));
            SeaSQL_setPortX(portx);
            break;
        case 'o':
            stary = ADJUST(stary + (addsub * STEP));
            SeaSQL_setStarY(stary);
            break;
        case 'l':
            starx = ADJUST(starx + (addsub * STEP));
            SeaSQL_setStarX(starx);
            break;
        case 'k':
            aft = ADJUST(aft + (addsub * STEP));
            SeaSQL_setAft(aft);
            break;
        }

        if(c == 'q') {
            break;
        }
    }

    /* Turn off drivers */
    SeaSQL_setPortX(0);
    SeaSQL_setPortY(0);
    SeaSQL_setStarX(0);
    SeaSQL_setStarY(0);
    SeaSQL_setAft(0);

    Seawolf_close();
    endwin();
    return 0;
}
