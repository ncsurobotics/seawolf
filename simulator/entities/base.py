
from OpenGL.GL import *
from OpenGL.GLUT import *

class Entity(object):

    def __init__(self, pos, color=(0.5,0.5,0.5), yaw_offset=0, yaw=0, pitch=0, roll=0):
        assert len(pos)==3
        assert len(color)==3 or len(color)==4
        self.pos = pos
        self.color = color
        self.yaw_offset = yaw_offset
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
        self.simulator = None

    def _register_simulator(self, simulator):
        self.simulator = simulator

    def step(self, dt):
        pass

    def pre_draw(self):
        #glMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.color)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslate(self.pos[0], self.pos[1], self.pos[2])
        glRotate(self.pitch, 0, 1, 0)
        glRotate(self.roll, 1, 0, 0)
        glRotate(self.yaw_offset, 0, 0, -1)
        glRotate(self.yaw, 0, 0, -1)

    def draw(self):
        self.pre_draw()
        self.post_draw()

    def post_draw(self):
        glPopMatrix()

class ModelEntity(Entity):
    def __init__(self, model, *args, **kwargs):
        self.model = model
        super(ModelEntity, self).__init__(*args, **kwargs)

    def draw(self):
        self.pre_draw()
        self.model.draw()
        self.post_draw()

class CubeEntity(Entity):
    def __init__(self, size, *args, **kwargs):
        self.size = size
        super(CubeEntity, self).__init__(*args, **kwargs)

    def draw(self):
        self.pre_draw()
        #glutWireCube(self.size)
        glutSolidCube(self.size)
        self.post_draw()
