from entities.base import VisionEntity

class Path(VisionEntity):

    camera_name = "down"

    def find(self, frame):

        # Randomised test code
        import time # imports are here so I don't forget to take them out
        from random import choice
        time.sleep(0.1)
        return choice([True, False])
