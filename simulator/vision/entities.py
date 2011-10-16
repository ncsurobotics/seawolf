
import xmlrpclib

class SimulatedEntity(object):

    entity_name = ""

    def __init__(self, camera):
        self.camera = camera
        self.xmlrpc_client = xmlrpclib.ServerProxy("http://localhost:2839")
        if not self.entity_name:
            raise NotImplementedError("SimulatedEntity must be subclassed and the entity_name class attribute overwritten.")

    def get_data(self):
        data = self.xmlrpc_client.find_entity(self.entity_name, self.camera)
        if data:
            return data
        else:
            return None

class GateEntity(object):
    entity_name = "gate"
