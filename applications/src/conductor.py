
from time import sleep
from subprocess import Popen

import seawolf

STATUS_LIGHT_OFF = 0
STATUS_LIGHT_BLINK = 1
STATUS_LIGHT_ON = 2

APPS_TO_START = [
    "./bin/depthpidpy",
    "./bin/yawpidpy",
    "./bin/pitchpidpy",
    "./bin/rollpidpy",
    "./bin/mixer",
]


def zero_thrusters():

    seawolf.var.set("DepthPID.Paused", 1)
    seawolf.var.set("PitchPID.Paused", 1)
    seawolf.var.set("YawPID.Paused", 1)

    seawolf.notify.send("THRUSTER_REQUEST", "Depth 0 0 0")
    seawolf.notify.send("THRUSTER_REQUEST", "Forward 0 0")

    seawolf.var.set("Port", 0)
    seawolf.var.set("Star", 0)
    seawolf.var.set("Bow", 0)
    seawolf.var.set("Stern", 0)
    seawolf.var.set("StrafeT", 0)
    seawolf.var.set("StrafeB", 0)


def main():

    seawolf.notify.filter(seawolf.FILTER_MATCH, "EVENT PowerKill")
    seawolf.notify.filter(seawolf.FILTER_MATCH, "EVENT SystemReset")

    seawolf.var.set("MissionReset", 0)
    seawolf.var.set("StatusLight", STATUS_LIGHT_OFF)
    zero_thrusters()

    running = False
    while True:
        _, event = seawolf.notify.get()

        if event == "SystemReset":

            if running:
                seawolf.logging.log(seawolf.ERROR, "Received SystemReset while running!")
                continue

            # Delay
            seawolf.var.set("StatusLight", STATUS_LIGHT_BLINK)
            for i in [3, 2, 1]:
                seawolf.logging.log(seawolf.DEBUG, "Preparing to start - %d" % i)
                sleep(1)

            # Start
            seawolf.notify.send("GO", "Mission Control")
            seawolf.var.set("StatusLight", STATUS_LIGHT_ON)
            running = True

        elif event == "PowerKill":

            if not running:
                seawolf.logging.log(seawolf.ERROR, "Received PowerKill while not running!")
                continue

            seawolf.var.set("StatusLight", STATUS_LIGHT_OFF)
            seawolf.logging.log(seawolf.DEBUG, "Killing...")
            seawolf.var.set("MissionReset", 1)
            zero_thrusters()

            # Wait for mission control to acknowledge reset
            while seawolf.var.get("MissionReset"):
                print "Thruster's zero'd. Waiting for mission reset"
                sleep(0.1)
            zero_thrusters()
            running = False

        else:
            seawolf.logging.log(seawolf.ERROR, 'Recieved invalid event "%s"' % event)


if __name__ == "__main__":

    seawolf.loadConfig("../conf/seawolf.conf")
    seawolf.init("Conductor")

    zero_thrusters()
    app_processes = {}
    for app_name in APPS_TO_START:
        app_processes[app_name] = Popen(app_name)
    sleep(2)

    try:
        main()
    except Exception:
        print "TERMINATING APPLICATIONS..."
        for app in app_processes.itervalues:
            app.terminate()
        raise
