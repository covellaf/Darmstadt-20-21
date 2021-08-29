from satsim import InvalidSimulatorState
from satsim import Logger, TimeKeeper, EventManager, Scheduler, Resolver,\
    LinkRegistry
from satsim import Component, Composite, Container, Publication
import simpy as sp


class Simulator(Composite, Publication):

    BUILDING = 0
    CONNECTING = 1
    INITIALISING = 2
    STANDBY = 3
    EXECUTING = 4
    STORING = 5
    RESTORING = 6
    RECONNECTING = 7
    EXITING = 8
    ABORTING = 9

    def __init__(self):
        self._containers = [
            Container("Models", "", self),
            Container("Services", "", self)
        ]

        self.env = sp.Environment()  # Create the environment

        # services
        self._logger = Logger(self)
        self._time_keeper = TimeKeeper(self)
        self._scheduler = Scheduler(self)
        self._event_manager = EventManager(self)
        self._resolver = Resolver(self)
        self._link_registry = LinkRegistry(self)

        self._init_entry_points = []

        self._state = self.BUILDING

    def publish(self):
        if self._state != self.BUILDING:
            return

        for service in self.get_container("Services").get_components():
            if service._state == Component.CREATED:
                service.publish(self)
                # TODO: call publish on all child components recursevly

        for model in self.get_container("Models").get_components():
            if model._state == Component.CREATED:
                model.publish(self)
                # TODO: call publish on all child components recursevly

    def configure(self):
        if self._state != self.BUILDING:
            return

        for service in self.get_container("Services").get_components():
            if service._state == Component.CREATED:
                service.publish(self)
            if service._state == Component.PUBLISHING:
                service.configure(self._logger, self._link_registry)
            # TODO: do this all child components recursevly

        for model in self.get_container("Models").get_components():
            if model._state == Component.CREATED:
                model.publish(self)
            if model._state == Component.PUBLISHING:
                model.configure(self._logger, self._link_registry)
            # TODO: do this all child components recursevly

    def connect(self):
        if self._state != self.BUILDING:
            return

        self._state = self.CONNECTING

        for service in self.get_container("Services").get_components():
            if service._state == Component.CREATED:
                service.publish(self)
            if service._state == Component.PUBLISHING:
                service.configure(self.logger, self.link_registry)
            if service._state == Component.CONFIGURED:
                service.connect(self)
            # TODO: do this all child components recursevly

        for model in self.get_container("Models").get_components():
            if model._state == Component.CREATED:
                model.publish(self)
            if model._state == Component.PUBLISHING:
                model.configure(self.logger, self.link_registry)
            if model._state == Component.CONFIGURED:
                model.connect(self)
            # TODO: do this all child components recursevly

        event_id = self._event_manager.query_event_id("LEAVE_CONNECTING")
        self._event_manager.emit(event_id)

        self._state = self.INITIALISING

        event_id = self._event_manager.query_event_id("ENTER_INITIALISING")
        self._event_manager.emit(event_id)

        for init_entry_point in self._init_entry_points:
            init_entry_point()
        self._init_entry_points = []

        event_id = self._event_manager.query_event_id("LEAVE_INITIALISING")
        self._event_manager.emit(event_id)

        self._state = self.STANDBY

        event_id = self._event_manager.query_event_id("ENTER_STANDBY")
        self._event_manager.emit(event_id)

    def initialise(self):
        if self._state != self.STANDBY:
            return

        event_id = self._event_manager.query_event_id("LEAVE_STANDBY")
        self._event_manager.emit(event_id)

        self._state = self.INITIALISING

        event_id = self._event_manager.query_event_id("ENTER_INITIALISING")
        self._event_manager.emit(event_id)

        for init_entry_point in self._init_entry_points:
            init_entry_point()
        self._init_entry_points = []

        event_id = self._event_manager.query_event_id("LEAVE_INITIALISING")
        self._event_manager.emit(event_id)

        self._state = self.STANDBY

        event_id = self._event_manager.query_event_id("ENTER_STANDBY")
        self._event_manager.emit(event_id)

    def run(self):
        if self._state != self.STANDBY:
            return

        event_id = self._event_manager.query_event_id("LEAVE_STANDBY")
        self._event_manager.emit(event_id)

        self._state = self.EXECUTING

        event_id = self._event_manager.query_event_id("ENTER_EXECUTING")
        self._event_manager.emit(event_id)

        # start the simulation
        self.env.process(self.run_simulation())
        self.env.run(until=12)

    def run_simulation(self):
        # new method
        scheduled_events = self._scheduler._scheduled_events

        while True:
            for key in scheduled_events.keys():
                if self.env.now == scheduled_events[key]['simulation_time']:
                    print("Function executed at", self.env.now)
                    scheduled_events[key]['entry_point'].execute()
                    print(f"the last event executed was {scheduled_events[key]['entry_point']}")
                    # print(type(scheduled_events[key]['entry_point']))
            yield self.env.timeout(1)

    def hold(self, immediate=False):
        pass

    def store(self, filename):
        pass

    def restore(self, filename):
        pass

    def reconnect(self, root):
        pass

    def exit(self):
        pass

    def abort(self):
        pass

    def get_state(self):
        return self._state

    def add_init_entry_point(self, entry_point):
        if self._state not in [self.BUILDING, self.CONNECTING, self.STANDBY]:
            return

        self.init_entry_points.append(entry_point)

    def add_model(self, model):
        if self._state not in [
                self.STANDBY, self.BUILDING,
                self.CONNECTING, self.INITIALISING]:
            raise InvalidSimulatorState()
        self.get_container("Models").add_component(model)

    def add_service(self, service):
        if self._state not in self.BUILDING:
            raise InvalidSimulatorState()
        self.services.append(service)

    def get_service(self, name):
        pass

    def get_logger(self):
        return self._logger

    def get_time_keeper(self):
        return self._time_keeper

    def get_scheduler(self):
        return self._scheduler

    def get_event_manager(self):
        return self._event_manager

    def get_resolver(self):
        return self._resolver

    def get_link_registry(self):
        return self._link_registry
