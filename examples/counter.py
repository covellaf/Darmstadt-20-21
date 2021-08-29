""" Counter Example
    This example is taken from SMP 2.0 Handbook, chapter 3
"""
import time
from datetime import timedelta

import satsim


class CounterModel(satsim.Model):

    def __init__(self, name, description, parent):
        super().__init__(name, description, parent)
        self.counter = 0
        self.entrypoint = satsim.EntryPoint("Counter Entrypoint")
        self.entrypoint.execute = lambda: self.count()

    def reset(self):
        self.counter = 0

    def count(self):
        self.counter += 1
        self.logger.log_debug(self, "Increase counter")

    def log_count(self):
        self.logger.log_info(self, "Counter value {}".format(self.counter))

    def configure(self, logger, link_registry):
        """Perform initial configuration."""
        if self._state != self.PUBLISHING:
            raise satsim.InvalidComponentState()

        self.logger = logger
        self.logger.log_info(self, "Counter Model is now configured")

        self._state = self.CONFIGURED

    def connect(self, simulator):
        """Connect to the simulator environment and other components"""
        if self._state != self.CONFIGURED:
            raise satsim.InvalidComponentState()

        self.scheduler = simulator.get_scheduler()
        self.scheduler.add_simulation_time_event(
            self.entrypoint, 1)  # I have changed timedelta(seconds=1)
        self.logger.log_info(self, "Counter Model is now connected")

        self._state = self.CONNECTED


# main()


# create simulator
simulator = satsim.Simulator()

# create model instance
counter_model = CounterModel("Counter", "Counter Model", simulator)

# add to models container
simulator.add_model(counter_model)

# simulator starting
simulator.publish()
simulator.configure()
simulator.connect()
simulator.initialise()

print("Simulation started")
simulator.run()
time.sleep(5)  # run for some time
simulator.exit()
print("Simulation finished")
