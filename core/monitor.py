import json


class Monitor(object):
    def __init__(self, simulation, checking_steps=10, include_machine_states=False):
        self.simulation = simulation
        self.env = simulation.env
        self.event_file = simulation.event_file
        self.events = []
        self.checking_steps = checking_steps
        self.include_machine_states = include_machine_states

    def run(self):
        while not self.simulation.finished:
            state = {
                'timestamp': self.env.now,
                'cluster_state': self.simulation.cluster.cluster_state
            }
            self.events.append(state)
            yield self.env.timeout(self.checking_steps)

        state = {
            'timestamp': self.env.now,
            'cluster_state': self.simulation.cluster.cluster_state
        }
        if self.include_machine_states:
            state['machine_states'] = self.simulation.cluster.machine_states
        self.events.append(state)

        self.write_to_file()

    def write_to_file(self):
        with open(self.event_file, 'w') as f:
            json.dump(self.events, f, indent=4)
