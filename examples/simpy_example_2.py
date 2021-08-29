# simpy test #2

import simpy as sp


# condition events can be concatenated by logical operator

def speaker(env):
    try:
        yield env.timeout(randint(25,30))
    except sp.Interrupt as interrupt:
        # return 'handout'
        print(interrupt.cause)

def moderator(env):
    for i in range(3):
        speaker_proc = env.process(speaker(env))
        # results is a dictionnary which contains all the
        # events that have been triggered
        results = yield speaker_proc | env.timeout(30)
        if speaker_proc not in results:
            speaker_proc.interrupt('No time left')

# simpy has shared resources
# 1. queue resources, processes can be sorted by priority
# 2. store resources, can store python objects

env = sp.Environment()
env.process(speaker(env))
env.process(moderator(env))
env.run()

# def main():
#     env = sp.Environment()
#     speaker(env)
#     moderator(env)
#     env.run()
#
# if __name__ == "__main__" :
#     main()
