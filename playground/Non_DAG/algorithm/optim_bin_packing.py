from asyncio import tasks

from core.alogrithm import Algorithm
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

from core.batch_algorithm import BatchAlgorithm

import random

"""Solve the Bin packing with Google OR tools"""


class OptimalBinPacking(BatchAlgorithm):

    def __init__(self, batch, solver_name='SCIP'):
        super().__init__(batch)
        # solver_name = "GLOP"
        self.solver_name = solver_name

    def __call__(self, cluster, clock):
        machines = cluster.machines
        solver = pywraplp.Solver.CreateSolver(self.solver_name)

        # sample_count = min(len(cluster.waiting_task_instances), self.batch)
        # sampled_tasks_instances = random.sample(cluster.waiting_task_instances, sample_count)

        # filter out the unplaceable tasks which size is larger than the server with most unused cpu resources
        machine_cpu_capacity = [machine.cpu for machine in machines]
        machine_ids = range(len(machine_cpu_capacity))
        max_machines_cpu = max(machine_cpu_capacity)

        tasks_instances = \
            [ task_instance for task_instance in cluster.waiting_task_instances if task_instance.cpu <= max_machines_cpu]
        task_cpu_demands = [task_instance.cpu for task_instance in tasks_instances]
        task_ids = range(len(task_cpu_demands))
        if len(task_cpu_demands) == 0:
            return [], []

        # x[i, b] = 1 if task i is packed in machine b.
        x = {}
        for i in task_ids:
            for b in machine_ids:
                x[i, b] = solver.BoolVar(f"x_{i}_{b}")

        # Assume one task only be placed into one machines
        for i in task_ids:
            solver.Add(sum(x[i, b] for b in machine_ids) <= 1)

        # The amount packed in each bin cannot exceed its capacity.
        for b in machine_ids:
            solver.Add(
                sum(x[i, b] * task_cpu_demands[i] for i in task_ids)
                <= machine_cpu_capacity[b]
            )

        #  Object to Maximize the cpu resources usage
        objective = solver.Objective()
        for i in task_ids:
            for b in machine_ids:
                objective.SetCoefficient(x[i, b], task_cpu_demands[i])
        objective.SetMaximization()
        print("start solve")
        status = solver.Solve()

        candidate_tasks = []
        candidate_machines = []

        if status == pywraplp.Solver.OPTIMAL:
            for i in task_ids:
                for b in machine_ids:
                    task = tasks_instances[i].task
                    machine = machines[b]
                    #  ignoring the memory and disk limitation
                    if x[i, b].solution_value() > 0 and machine.accommodate(task):
                        candidate_tasks.append(task)
                        candidate_machines.append(machine)

        return candidate_machines, candidate_tasks
