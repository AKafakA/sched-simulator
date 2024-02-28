import os
import time
import numpy as np
import tensorflow as tf
import sys
from core.machine import MachineConfig
from playground.Non_DAG.algorithm.random_algorithm import RandomAlgorithm
from playground.Non_DAG.algorithm.tetris import Tetris
from playground.Non_DAG.algorithm.first_fit import FirstFitAlgorithm
from playground.Non_DAG.algorithm.optim_bin_packing import OptimalBinPacking

from playground.Non_DAG.utils.csv_reader import CSVReader
from playground.Non_DAG.utils.tools import average_completion
from playground.Non_DAG.utils.episode import Episode

sys.path.append('..')
os.environ['CUDA_VISIBLE_DEVICES'] = ''

np.random.seed(41)
tf.random.set_seed(41)

# ************************ Machine configs ************************
# Check the EC2 example: https://aws.amazon.com/ec2/instance-types/?nc1=h_ls
# Ignoring the memory limitation by manually increasing the memory capacity to xlarge number

m7g_medium = MachineConfig(1, 1000, 1000)
m7g_xlarge = MachineConfig(8, 1000, 1000)
m7g_metal = MachineConfig(64, 1000, 1000)
# ************************************************

# ************************ Parameters Setting Start ************************
machines_number_m7g_medium = 7
machines_number_m7g_xlarge = 4
machines_number_m7g_metal = 2
jobs_len = 20
jobs_csv = '../jobs_files/jobs.csv'
# ************************ Parameters Setting End ************************


machine_configs = []
machine_configs.extend([m7g_medium] * machines_number_m7g_medium)
machine_configs.extend([m7g_xlarge] * machines_number_m7g_xlarge)
machine_configs.extend([m7g_metal] * machines_number_m7g_metal)

csv_reader = CSVReader(jobs_csv)
jobs_configs = csv_reader.generate(0, jobs_len)

tic = time.time()
algorithm = RandomAlgorithm()
episode = Episode(machine_configs, jobs_configs, algorithm, "../logs/random")
episode.run()
print("Algorithm: Random",
      " Execution time: " + str(time.time() - tic) +
      " Ave completion time: " + str(average_completion(episode)))

tic = time.time()
algorithm = FirstFitAlgorithm()
episode = Episode(machine_configs, jobs_configs, algorithm, "../logs/first_fit")
episode.run()
print("Algorithm: First fit " +
      " Execution time: " + str(time.time() - tic) +
      " Ave completion time: " + str(average_completion(episode)))

tic = time.time()
algorithm = Tetris()
episode = Episode(machine_configs, jobs_configs, algorithm, "../logs/tetris")
episode.run()
print("Algorithm: Tetris" +
      " Execution time: " + str(time.time() - tic) +
      " Ave completion time: " + str(average_completion(episode)))

tic = time.time()
algorithm = RandomAlgorithm()
# Large batch number means do the scheduling without batch size requirement
batch = 10000000
batch_algorithm = OptimalBinPacking(batch=batch)
episode = Episode(machine_configs, jobs_configs, algorithm, "../logs/optimal", batch_algorithm=batch_algorithm)
episode.run()
print("Algorithm: Optimal" +
      " Execution time: " + str(time.time() - tic) +
      " Ave completion time: " + str(average_completion(episode)))
