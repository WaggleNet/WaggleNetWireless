#"module" is not the final name for this interface
#every data generating device (camera, microphone, thermometer) 
#should have its own module class which implements setup and
#poll functions

import random
import time

id_length = 16

#dummy class representing a generic sensor, not required
class exampleSensor():
    def read_data(self):
        data = [random.randint(0, 9999) for i in range(0, 10)]
        return data

class exampleModule():
    module_name = "example" #put the name of your sensor/project here
    sensor = None
    polling_interval = .5 #time between polls in seconds
    last_poll = time.monotonic()

    def __init__(self):
        if(len(self.module_name) > 16):
            print("module name should be less than 16 chars long")
        self.module_id = self.module_name[0:min(len(self.module_name), id_length)]
        self.module_id += (id_length - len(self.module_id)) * " "
        self.module_id = bytearray(self.module_id, encoding="ascii")
        print(f"instance of {self.module_name} created with id {self.module_id}")

    def setup(self):
        self.sensor = exampleSensor()

#don't need to modify this
    def wrap_poll(self):
        if ((time.monotonic() - self.last_poll) > self.polling_interval):
            self.last_poll = time.monotonic()
            data = bytearray(self.poll())
            header = self.module_id + len(data).to_bytes(4)
            return header + data
        return None


    def poll(self):
        sensor_data = self.sensor.read_data()
        return sensor_data