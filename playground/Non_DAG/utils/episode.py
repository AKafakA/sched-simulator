import simpy
from markdown.preprocessors import Preprocessor

from core.cluster import Cluster
from core.scheduler import Scheduler
from core.broker import Broker
from core.simulation import Simulation


class Episode(object):
    def __init__(self, machine_configs, task_configs, algorithm, event_file, batch_algorithm=None):
        self.env = simpy.Environment()
        cluster = Cluster()
        cluster.add_machines(machine_configs)

        task_broker = Broker(self.env, task_configs)

        scheduler = Scheduler(self.env, algorithm, batch_algorithm=batch_algorithm)

        self.simulation = Simulation(self.env, cluster, task_broker, scheduler, event_file)

    def run(self):
        self.simulation.run()
        self.env.run()
