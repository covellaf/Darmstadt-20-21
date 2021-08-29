import simpy as sp


def clock(env):
    # This function should be in simulator.run
    while True:
        for k in scheduled_events.keys():
            if env.now == scheduled_events[k]['simulation_time']:
                print("Function executed at", env.now)
                # call entrypoint = scheduled_events[k]['entry_point'] -->
                # then use the execute function of EntryPoint class

        yield env.timeout(1)


def add_simulation_time_event(
        event_id, entry_point, simulation_time, cycle_time=0, repeat=0):
    # I put event_id to try
    scheduled_events[event_id] = {
            'entry_point': entry_point,
            'simulation_time': simulation_time,
            'cycle_time': cycle_time,
            'repeat': repeat}


scheduled_events = {}

add_simulation_time_event(1, 2, 3, 4, 5)
add_simulation_time_event(2, 4, 6, 8, 10)
add_simulation_time_event(3, 5, 7, 9, 3)


env = sp.Environment()
env.process(clock(env))
endsimulation = 10
env.run(until=endsimulation)
