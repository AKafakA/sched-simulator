import os
import matplotlib.pyplot as plt
import json


path = '../logs/'

cpu_utilization = {}
for filename in os.listdir(path):
    if filename:
        ls = []
        cpu_utilization[filename] = ls
        with open(os.path.join(path, filename)) as f:
            d = json.load(f)
            for record in d:
                ls.append(record['cluster_state']['cpu_usage'])

max_timestamp = max([len(cpu_usages) for cpu_usages in cpu_utilization.values()])
timestamps = range(max_timestamp)

# interesting_cpu_utilization = ['first_fit', 'random']
interesting_cpu_utilization = cpu_utilization.keys()

for key, cpu_usages in cpu_utilization.items():
    fills = [cpu_usages[-1]] * (max_timestamp - len(cpu_usages))
    cpu_usages.extend(fills)
    if key in interesting_cpu_utilization:
        plt.plot(timestamps, cpu_usages, label=key)
    print(key + " average cpu usage: " + str(sum(cpu_usages) / len(cpu_usages)))

plt.legend(loc='best')
plt.savefig('./figures/cpu_utilization_real_20_jobs.png')




