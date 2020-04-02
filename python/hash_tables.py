import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_test_values(size):
    """
    Creates a numpy array of integers (0 ... size) randomly arranged
    """
    return np.random.default_rng().choice(size, size = (size), replace = False)

def create_lookup_values(size, num_lookups):
    """
    Creates a numpy array of length num_lookups, filled with non-repeating integers within (0 ... size)
    """
    return np.random.default_rng().choice(size, size = (num_lookups), replace = False)

def compute_container_lookups(items_in_container, container):
    for item in items_in_container:
        if item in container:
            pass

def compare_hash_vs_list_lookups():
    """
    Shows the difference between using a hash table (dict or set) and using a list to process lookups
    """

    time_to_run = []
    step_size = 1000
    num_data_points = 100
    max_size = step_size * num_data_points

    num_trials = 10
    num_lookups = 25

    for size in range(num_lookups, max_size, step_size + num_lookups):

        # initialize containers with random data of length 'size'
        test_values = create_test_values(size)
        test_lookups = create_lookup_values(size, num_lookups)
        test_list = list(test_values)
        test_set = set(test_values)

        # compute average lookup time on the list container
        start = time.time()
        for trial in range(num_trials):
            compute_container_lookups(test_lookups, test_list)
        list_lookup_time = (time.time() - start) / (size * num_trials)

        # compute average lookup time on the set container
        start = time.time()
        for trial in range(num_trials):
            compute_container_lookups(test_lookups, test_set)
        set_lookup_time = (time.time() - start) / (size * num_trials)

        # compute average lookup time, amortizing conversion of a list into a set
        start = time.time()
        for trial in range(num_trials):
            set_for_lookups = set(test_list)
            compute_container_lookups(set_for_lookups, test_set)
        set_conversion_and_lookup_time = (time.time() - start) / (size * num_trials)

        # add data to list
        time_to_run += [
            (size, 'List Lookup', list_lookup_time)
            ,(size, 'Set Lookup', set_lookup_time)
            ,(size, 'Set Creation and Lookup', set_conversion_and_lookup_time)
        ]

    # build DataFrame with data
    run_times = pd.DataFrame(data = time_to_run, columns = ['Size of Container', 'Operation', 'Duration'])

    # plot data
    sns.lmplot(x = 'Size of Container', y = 'Duration', data = run_times, hue = 'Operation')

    plt.legend()
    plt.title('Hash vs List Average Lookup Time')
    plt.xlabel('Container Size')
    plt.ylabel(f'Average Time for {num_lookups} Lookups')
    plt.show()

if __name__ == '__main__':
    compare_hash_vs_list_lookups()
