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
    """
    Performs lookup of each item in 'items_in_container' within 'container'
    """
    for item in items_in_container:
        if item in container:
            pass

def compare_hash_vs_list_lookups():
    """
    Shows the difference between using a hash table (dict or set) and using a list to process lookups
    """
    time_to_run = []

    num_trials = 10

    num_lookups_start = 5
    num_lookups_step_size = 7
    num_lookups_data_points = 5
    num_lookups_max = num_lookups_start + num_lookups_step_size * num_lookups_data_points

    num_data_points = 100
    step_size = 1000
    max_size = num_lookups_max + step_size * num_data_points

    for num_lookups in range(num_lookups_start, num_lookups_max, num_lookups_step_size):
        for size in range(num_lookups_max, max_size, step_size):

            # initialize containers with random data of length 'size'
            test_values = create_test_values(size)
            test_lookups = create_lookup_values(size, num_lookups)
            test_list = list(test_values)
            test_set = set(test_values)

            # compute average lookup time on the list container
            start = time.time()
            for trial in range(num_trials):
                compute_container_lookups(test_lookups, test_list)
            list_lookup_time = (time.time() - start) / (num_lookups * num_trials)

            # compute average lookup time on the set container
            start = time.time()
            for trial in range(num_trials):
                compute_container_lookups(test_lookups, test_set)
            set_lookup_time = (time.time() - start) / (num_lookups * num_trials)

            # compute average lookup time, amortizing conversion of a list into a set
            start = time.time()
            for trial in range(num_trials):
                set_for_lookups = set(test_list)
                compute_container_lookups(set_for_lookups, test_set)
            set_conversion_and_lookup_time = (time.time() - start) / (num_lookups * num_trials)

            # add data to list
            time_to_run += [
                (num_lookups, size, 'List Lookup', list_lookup_time)
                ,(num_lookups, size, 'Set Lookup', set_lookup_time)
                ,(num_lookups, size, 'Set Creation and Lookup', set_conversion_and_lookup_time)
            ]

    # build DataFrame with data
    run_times = pd.DataFrame(data = time_to_run, columns = ['Number of Lookups', 'Size of Container', 'Operation', 'Duration'])

    # plot data with linear model fit
    sns.lmplot(x = 'Size of Container', y = 'Duration', data = run_times, hue = 'Operation', col = 'Number of Lookups', legend = False)

    # set labels and title and plot data
    plt.xlabel('Container Size')
    plt.ylabel(f'Average Time for {num_lookups} Lookups')
    plt.subplots_adjust(top = 0.7, right = 0.5)
    plt.legend(bbox_to_anchor = (1.05, 1), loc = 2, borderaxespad = 0.)
    plt.tight_layout()
    plt.show()

def generate_test_values_visualization(size):
    """
    Plot a visualization of the test data generated for profiling
    """
    values = create_test_values(size)
    sns.scatterplot(x = range(size), y = values)
    plt.title(f'Test Values, Size = {size}')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.show()

def generate_test_values_with_lookups_visualization(size, num_lookups):
    """
    Plot a visualization of the test data and lookup data points generated for profiling
    """
    values = create_test_values(size)
    lookups = set(create_lookup_values(size, num_lookups))
    df = pd.DataFrame(index = range(size), data = values, columns = ['Value'])
    df.reset_index(inplace = True)
    df['Lookup'] = df['Value'].apply(lambda x: 1 if x in lookups else 0)
    plot = sns.scatterplot(data = df, x = 'index', y = 'Value', hue = 'Lookup', legend = False)
    plt.title('Test Values with Lookups Highlighted')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.show()

if __name__ == '__main__':

    compare_hash_vs_list_lookups()
