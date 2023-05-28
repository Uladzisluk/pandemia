import random
import time

import numpy as np
from threading import Thread
import warnings
import matplotlib.pyplot as plt
from matplotlib import animation

warnings.simplefilter("ignore", UserWarning)
nr_of_people = 1000
nr_of_infected_people = 3
dt = 0.003
L = 1
size = 20

particles = np.zeros(nr_of_people, dtype=[("position", float, 2),
                                          ("velocity", float, 2),
                                          ("force", float, 2),
                                          ("infected", int)])

particles["position"] = np.random.uniform(0.1, L-0.1, (nr_of_people, 2))
particles["velocity"] = np.zeros((nr_of_people, 2))
infected_indexes = random.choices(range(0, nr_of_people), k=nr_of_infected_people)
for i in infected_indexes:
    particles["infected"][i] = 1

class AnimatedScatter(object):
    def __init__(self):
        self.scat = None
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(0, L), ylim=(0, L))
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=15, init_func=self.setup_plot)

    def setup_plot(self):
        self.scat = self.ax.scatter(particles["position"][:, 0], particles["position"][:, 1], s=size)
        return self.scat

    def update(self, i):
        particles["force"] = np.random.uniform(-2, 2., (nr_of_people, 2))
        particles["velocity"] = particles["velocity"] + particles["force"]*dt
        particles["position"] = particles["position"] + particles["velocity"]*dt
        for i in range(0, nr_of_people):
            if particles["position"][i, 0] - size < 0 or particles["position"][i, 0] + size >= 1:
                particles["position"][i, :] = particles["position"][i, :] - particles["velocity"][i, :]*dt
                particles["velocity"][i, :] = np.zeros((1, 2))
            elif particles["position"][i, 1] - size < 0 or particles["position"][i, 1] + size >= 1:
                particles["position"][i, :] = particles["position"][i, :] - particles["velocity"][i, :]*dt
                particles["velocity"][i, :] = np.zeros((1, 2))
        self.scat.set_offsets(particles["position"])
        return self.scat


a = AnimatedScatter()
plt.show()
