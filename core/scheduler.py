class Scheduler(object):
    def __init__(self, env, algorithm, batch_algorithm=None):
        self.batch_algorithm = batch_algorithm
        self.batch = batch_algorithm.batch if batch_algorithm is not None else 1
        self.env = env
        self.algorithm = algorithm
        self.simulation = None
        self.cluster = None
        self.destroyed = False
        self.valid_pairs = {}
        self.preprocessor = None
        self.timestamp_since_last_batch = env.now
        self.max_batch_waiting_time = 1

    def attach(self, simulation):
        self.simulation = simulation
        self.cluster = simulation.cluster
        if self.preprocessor is not None:
            self.cluster = self.preprocessor(self.cluster)

    def make_decision(self):
        while True:
            if self.batch <= 1 or len(self.cluster.waiting_task_instances) <= 1:
                machine, task = self.algorithm(self.cluster, self.env.now)
                if machine is None or task is None:
                    break
                else:
                    task.start_task_instance(machine)
            # elif (self.batch <= len(self.cluster.waiting_task_instances)
            #       or (self.env.now - self.timestamp_since_last_batch) > self.max_batch_waiting_time):
            elif self.batch > 1:
                machines, tasks = self.place_in_batch()
                if len(tasks) == 0:
                    break
                print("waiting task instances before place:" + str(len(self.cluster.waiting_task_instances)))
                for task, machine in zip(tasks, machines):
                    task.start_task_instance(machine)
                # self.timestamp_since_last_batch = self.env.now
                print("waiting task instances after place:" + str(len(self.cluster.waiting_task_instances)))
                break
            else:
                break

    def place_in_batch(self):
        machines, tasks_instances = self.batch_algorithm(self.cluster, self.env.now)
        return machines, tasks_instances

    def run(self):
        while not self.simulation.finished:
            self.make_decision()
            yield self.env.timeout(1)
        self.destroyed = True
