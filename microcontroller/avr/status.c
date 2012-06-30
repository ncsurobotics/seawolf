
#include <sw.h>

static int status_value = 200;

void update_status(int counter) {
    if(counter % 200 >= status_value) {
        PORTA.OUTSET = 1 << 2;
    } else {
        PORTA.OUTCLR = 1 << 2;
    }
}

void set_status(int value) {
    status_value = value;
}

void init_status(void) {
    PORTA.DIRSET = 1 << 2;
}
