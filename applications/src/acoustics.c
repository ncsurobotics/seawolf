
#include "seawolf.h"
#include "seawolf3.h"

#define SET1 "Acoustics.Delay.AC"
#define SET2 "Acoustics.Delay.BC"

#define SPEED_OF_SOUND 1484 /* m/s */
#define HYDROPHONE_SPACING 1.17 /* m */
#define TIME_DELAY ((int)(HYDROPHONE_SPACING / SPEED_OF_SOUND)) /* s */
#define SAMPLE_RATE (96 * 1024) /* Hz */
#define SET_POINT (TIME_DELAY * SAMPLE_RATE) /* Unitless */

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Acoustics Controller");

    PID* pid = PID_new(SET_POINT, 1.0, 0.0, 0.0);
    int avg_delay;
    float out;

    Notify_filter(FILTER_MATCH, "UPDATE Acoustics.Delay");

    Var_set("Rot.Mode", ROT_MODE_ANGULAR);

    while(true) {
        /* Get new delay */
        Notify_get(NULL, NULL);
        avg_delay = (Var_get(SET1) + Var_get(SET2)) / 2;

        /* Update PID */
        out = PID_update(pid, avg_delay);

        /* Set rotational PID target */
        Var_set("Rot.Angular.Target", Var_get("SEA.Yaw") + out);
    }

    Seawolf_close();
    return 0;
}
