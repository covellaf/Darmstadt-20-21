import simpy as sp

simulation_time = {}

def clock(env):
    while True: # env.now != endsimulation:
        if env.now in simulation_time.keys():
            print("The function is going to be executed at", env.now)
            simulation_time[env.now]()  # Executes the function
            yield env.timeout(1)
        else:
            print("Time is passing. Now is", env.now)
            yield env.timeout(1)

def add_simulation_time(moment, model):
    if moment not in simulation_time.keys():
        simulation_time[moment] = model


def addition():
    x = 1
    y = 8
    z = x + y
    print("--> The result is ", z)

def printer():
    print("--> Hello World")

def result():
    x = 2
    y = 15
    z = 23
    p = x*y + z
    print("--> The result is", p)


# def main():

# Add simulation time of Models
add_simulation_time(3, addition)
add_simulation_time(8, printer)
add_simulation_time(16, result)

    # Start simulation
env = sp.Environment()
env.process(clock(env))
endsimulation = 20
env.run(until=endsimulation)

# if __name__ == "__main__" :
#     main()
