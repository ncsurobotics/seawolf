
#include "seawolf.h"

#include <stdbool.h>

static struct {
    enum {
        UNKNOWN,
        START,
        GATE,
        BUOY,
        BARBEDWIRE,
        BOMBINGRUN,
        MACHINEGUN,
        BRIEFCASE
    } location;
} state;

static int doGate(void) {
    SeaSQL_setVisionTarget(VISIONTARGET_GATE);
    SeaSQL_setSetPointSource(SETPOINT_SOURCE_VISION);
    Notify_send("GO", "Gate");
    Notify_get(NULL, NULL);
    return 0;
}

static int doHitBuoy(void) {
    Notify_send("GO", "HitBuoy");
    // -
    Notify_get(NULL, NULL);
    return 0;
}

static int doBarbedWire(void) {
    Notify_send("GO", "BarbedWire");
    // -
    Notify_get(NULL, NULL);
    return 0;
}

static int doBombingRun(void) {
    Notify_send("GO", "BombingRun");
    // -
    Notify_get(NULL, NULL);
    return 0;
}

static int doMachineGunNest(void) {
    Notify_send("GO", "MachineGunNest");
    // -
    Notify_get(NULL, NULL);
    return 0;
}

static int doBriefcase(void) {
    Notify_send("GO", "Briefcase");
    // -
    Notify_get(NULL, NULL);
    return 0;
}

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("Mission Controller");

    /* Overall mission */
    TaskQueue* mission;

    /* Major tasks */
    Task *t_gate,
         *t_hitBuoy,
         *t_barbedWire,
         *t_bombingRun,
         *t_machineGunNest,
         *t_briefcase;

    /* Initialize global state */
    state.location = START;

    /* Initialize mission */
    mission = TaskQueue_new();
    
    /* Initialize first tier tasks */
    t_gate = Task_new(doGate);
    t_hitBuoy = Task_new(doHitBuoy);
    t_barbedWire = Task_new(doBarbedWire);
    t_bombingRun = Task_new(doBombingRun);
    t_machineGunNest = Task_new(doMachineGunNest);
    t_briefcase = Task_new(doBriefcase);
    
    /* Add tasks to queue */
    TaskQueue_addTask(mission, t_gate);
    TaskQueue_addTask(mission, t_hitBuoy);
    TaskQueue_addTask(mission, t_barbedWire);
    TaskQueue_addTask(mission, t_bombingRun);
    TaskQueue_addTask(mission, t_machineGunNest);
    TaskQueue_addTask(mission, t_briefcase);

    Notify_filter(FILTER_ACTION, "DONE");

    /* Run mission */
    TaskQueue_run(mission);

    /* Stop */
    SeaSQL_setSetPointSource(SETPOINT_SOURCE_OVERRIDE);
    SeaSQL_setSetPointOverride_Theta(0.0);
    SeaSQL_setSetPointOverride_Phi(0.0);
    SeaSQL_setSetPointOverride_Rho(0.0);

    Seawolf_close();
    return 0;
}
