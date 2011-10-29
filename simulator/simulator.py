
from __future__ import division
from time import time
import socket
from multiprocessing.connection import Listener

class Simulator(object):

    def __init__(self, interface, robot, entities=[], bind_address="localhost", bind_port=3829):

        self.interface = interface
        self.robot = robot
        self.entities = entities
        self.bind_address = bind_address
        self.bind_port = bind_port

        self.interface.register_simulator(self)
        self.add_entity(self.robot)
        self.last_step_time = None
        self.searching_entities = []
        self.last_capture_time = time()
        self.camera_frame_rate = 2

        # Listen for mission control on socket
        self.listener = Listener((self.bind_address, self.bind_port))
        self.listener._listener._socket.settimeout(0.01)  # Nonblocking self.listener.accept
        self.connection = None  # Connection to mission control

    def add_entity(self, entity):
        entity._register_simulator(self)
        self.entities.append(entity)

    def add_entities(self, entities):
        self.entities.extend(entities)

    def handle_pipe(self):

        # Attempt connection if not connected
        if self.connection is None:
            try:
                self.connection = self.listener.accept()
            except socket.timeout:
                self.connection = None

        # Get new entity search list
        if self.connection:
            try:
                while self.connection.poll():
                    self.searching_entities = self.connection.recv()
            except EOFError:
                # Other end has closed
                self.searching_entities = []
                self.connection = None

    def entity_search(self):
        """
        Look for entities in self.searching_entities and send results through
        pipe.
        """

        # Only capture every 1/self.camera_frame_rate secs
        t = time()
        if t < self.last_capture_time + 1/self.camera_frame_rate:
            return
        self.last_capture_time = t

        # Call entity.find for each entity
        data_list = []
        for entity in self.searching_entities:
            entity_data = self.robot.find_entity(entity)
            if entity_data:
                data_list.append( (entity, entity_data) )

        # Send data
        # self.searching_entities should be empty if self.connection=None, so
        # there is no danger of sending data when not connected.
        if data_list:
            self.connection.send(data_list)

    def run(self, delay=0.05):
        self.last_step_time = time()
        self.interface.run(delay)

    def step(self, dt=None):

        self.handle_pipe()
        self.entity_search()

        t = time()
        if not dt:
            dt = t - self.last_step_time

        for entity in self.entities:
            entity.step(dt)

        self.last_step_time = t
