
import seawolf as sw

__all__ = ["mixer"]


class Mixer(object):

    def set_forward(self, rate):
        sw.notify.send("THRUSTER_REQUEST", "Forward %.4f" % (rate,))

    def set_strafet(self, rate):
        sw.notify.send("THRUSTER_REQUEST", "StrafeT %.4f" % (rate,))

    def set_strafeb(self, rate):
        sw.notify.send("THRUSTER_REQUEST", "StrafeB %.4f" % (rate,))

    def set_roll(self, rate):
        sw.notify.send("THRUSTER_REQUEST", "Roll %.4f" % (rate,))

    def set_yaw(self, rate):
        sw.notify.send("THRUSTER_REQUEST", "Yaw %.4f" % (rate,))

    def set_depth(self, rate):
        sw.notify.send("THRUSTER_REQUEST", "Depth %.4f" % (rate,))

    def set_pitch(self, rate):
        sw.notify.send("THRUSTER_REQUEST", "Pitch %.4f" % (rate,))

    forward = property(lambda self: 0, set_forward)
    strafet = property(lambda self: 0, set_strafet)
    strafeb = property(lambda self: 0, set_strafeb)
    yaw = property(lambda self: 0, set_yaw)
    depth = property(lambda self: 0, set_depth)
    pitch = property(lambda self: 0, set_pitch)

mixer = Mixer()
