from __future__ import division
import seawolf
import math

thruster_cap = .4
ACTIVE_REGION_SIZE = 10 #degrees


def thruster_log(mv):
    if(math.fabs(mv) < 0.01):
        return 0.0
    return (mv / math.fabs(mv)) * math.log(math.fabs(mv) + 1, 2)


def in_range(a, x, b):
    if(x < a):
        return a
    elif(x > b):
        return b
    else:
        return x


def dataOut(mv):
    out = in_range(-thruster_cap, thruster_log(mv), thruster_cap)
    seawolf.notify.send("THRUSTER_REQUEST", "Yaw {}".format(out))


def angleError(a1, a2):
    error = a2 - a1

    if(math.fabs(error) > 180):
        if(error < 0):
            return (360.0 - math.fabs(error))
        return -(360.0 - math.fabs(error))

    return error


def main():
    seawolf.loadConfig("../conf/seawolf.conf")
    seawolf.init("Yaw PID")

    # initialize system variables for yaw PID system
    seawolf.var.subscribe("YawPID.p")
    seawolf.var.subscribe("YawPID.i")
    seawolf.var.subscribe("YawPID.d")
    seawolf.var.subscribe("YawPID.Heading")
    seawolf.var.subscribe("YawPID.Paused")
    seawolf.var.subscribe("SEA.Yaw")

    yaw = seawolf.var.get("SEA.Yaw")
    paused = seawolf.var.get("YawPID.Paused")
    heading = seawolf.var.get("YawPID.Heading")
    yaw = seawolf.var.get("SEA.Yaw")

    pid = seawolf.PID(
        0.0,
        seawolf.var.get("YawPID.p"),
        seawolf.var.get("YawPID.i"),
        seawolf.var.get("YawPID.d")
    )

    # set active region (region where response of the robot
    # is practically linear). Outside this region, thrusters
    # would be maxed out, and the ITerm would get staturated.
    # Outside this region, the we use PD control. Inside this
    # region, we use PID control.
    pid.setActiveRegion(ACTIVE_REGION_SIZE)
    pid.setDerivativeBufferSize(4)

    dataOut(0.0)
    mv = 0.0

    while(True):

        # wait for all variables to update
        seawolf.var.sync()

        # if seawolf's yaw has changed, save it to the local yaw variable.
        if seawolf.var.stale("SEA.Yaw"):
            yaw = seawolf.var.get("SEA.Yaw")

        # if PID controller's parameters have changed, update pid settings and reset controller
        if (seawolf.var.stale("YawPID.p") or seawolf.var.stale("YawPID.i") or seawolf.var.stale("YawPID.d")):

            pid.setCoefficients(
                seawolf.var.get("YawPID.p"),
                seawolf.var.get("YawPID.i"),
                seawolf.var.get("YawPID.d")
            )
            pid.resetIntegral()

        # if user has (possibly) modified seawolf's target heading, store the value
        # and unpause the yaw PID. The unpausing may have been done in order to accomodate
        # functionality whereby a user-level change to yaw PID heading will automatically,
        # take the robot out of pause mode. This is a means of saving the user from having
        # to manually unpause the robot to make changes, which would be somewhat un-intuitive
        # and bound cause confusion.
        if (seawolf.var.poked("YawPID.Heading")):
            heading = seawolf.var.get("YawPID.Heading")

            # if yawPID has been paused, unpause it.
            if paused:
                seawolf.var.set("YawPID.Paused", 0.0)

        # if Yaw PID pause state has changed, store it's value
        if (seawolf.var.stale("YawPID.Paused")):
            paused = seawolf.var.get("YawPID.Paused")

            # if paused, zero yaw thrusters and notify user
            if paused:
                dataOut(0.0)
                seawolf.notify.send("PIDPAUSED", "Yaw")
                pid.pause()

        # go ahead and run PID and output new thruster value if unpaused.
        if not paused:
            mv = pid.update(angleError(heading, yaw))
            dataOut(mv)

    seawolf.close()

if __name__ == "__main__":
    main()
