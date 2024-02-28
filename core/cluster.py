from core.machine import Machine


class Cluster(object):
    def __init__(self):
        self.machines = []
        self.jobs = []

    @property
    def unfinished_jobs(self):
        ls = []
        for job in self.jobs:
            if not job.finished:
                ls.append(job)
        return ls

    @property
    def unfinished_tasks(self):
        ls = []
        for job in self.jobs:
            ls.extend(job.unfinished_tasks)
        return ls

    @property
    def ready_unfinished_tasks(self):
        ls = []
        for job in self.jobs:
            ls.extend(job.ready_unfinished_tasks)
        return ls

    @property
    def tasks_which_has_waiting_instance(self):
        ls = []
        for job in self.jobs:
            ls.extend(job.tasks_which_has_waiting_instance)
        return ls

    @property
    def ready_tasks_which_has_waiting_instance(self):
        ls = []
        for job in self.jobs:
            ls.extend(job.ready_tasks_which_has_waiting_instance)
        return ls

    @property
    def finished_jobs(self):
        ls = []
        for job in self.jobs:
            if job.finished:
                ls.append(job)
        return ls

    @property
    def finished_tasks(self):
        ls = []
        for job in self.jobs:
            ls.extend(job.finished_tasks)
        return ls

    @property
    def waiting_task_instances(self):
        task_instances = []
        for job in self.jobs:
            task_instances.extend(job.waiting_task_instances)
        return task_instances

    @property
    def running_task_instances(self):
        task_instances = []
        for machine in self.machines:
            task_instances.extend(machine.running_task_instances)
        return task_instances

    def add_machines(self, machine_configs):
        for machine_config in machine_configs:
            machine = Machine(machine_config)
            self.machines.append(machine)
            machine.attach(self)

    def add_job(self, job):
        self.jobs.append(job)

    @property
    def cpu(self):
        return sum([machine.cpu for machine in self.machines])

    @property
    def memory(self):
        return sum([machine.memory for machine in self.machines])

    @property
    def disk(self):
        return sum([machine.disk for machine in self.machines])

    @property
    def cpu_capacity(self):
        return sum([machine.cpu_capacity for machine in self.machines])

    @property
    def memory_capacity(self):
        return sum([machine.memory_capacity for machine in self.machines])

    @property
    def disk_capacity(self):
        return sum([machine.disk_capacity for machine in self.machines])

    @property
    def cluster_state(self):
        return {
            'arrived_jobs': len(self.jobs),
            'unfinished_jobs': len(self.unfinished_jobs),
            'finished_jobs': len(self.finished_jobs),
            'unfinished_tasks': len(self.unfinished_tasks),
            'finished_tasks': len(self.finished_tasks),
            'running_task_instances': len(self.running_task_instances),
            'cpu_usage': (self.cpu_capacity - self.cpu) / self.cpu_capacity,
            'memory_usage': (self.memory_capacity - self.memory) / self.memory_capacity,
            'disk_usage': (self.disk_capacity - self.disk) / self.disk_capacity,
        }

    @property
    def machine_states(self):
        return [machine.state for machine in self.machines]
