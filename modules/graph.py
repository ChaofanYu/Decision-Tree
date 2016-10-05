from random import shuffle
from ID3 import *
from operator import xor
from parse import parse
import matplotlib.pyplot as plt
import os.path
from pruning import validation_accuracy
import random

# NOTE: these functions are just for your reference, you will NOT be graded on their output
# so you can feel free to implement them as you choose, or not implement them at all if you want
# to use an entirely different method for graphing

def get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, pct):
    '''
    get_graph_accuracy_partial - Given a training set, attribute metadata, validation set, numerical splits count, and percentage,
    this function will return the validation accuracy of a specified (percentage) portion of the trainging setself.
    '''
    data_set = []
    size = int(len(train_set) * pct)
    data_set = random.sample(train_set, size)
    #print size
    #for i in range(size - 1):
    #    data_set.append(train_set[i])
    #print "train_set"
    #print train_set
    tree = ID3(data_set, attribute_metadata, numerical_splits_count, 3)
    result = validation_accuracy(tree,validate_set)
    #print "result"
    #print result
    return result

    

def get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, iterations, pcts):
    '''
    Given a training set, attribute metadata, validation set, numerical splits count, iterations, and percentages,
    this function will return an array of the averaged graph accuracy partials based off the number of iterations.
    '''  
    result = []
    #print "pcts"
    #print pcts
    for j in pcts:
        sum = 0.0
        for i in range(iterations):
            size = int(len(train_set) * j - 1)
            #print len(train_set)
            print size
            #data_set = random.sample(train_set, size)
            #print "data_set"
            #print data_set
            acc_value = get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, j)
            sum = sum + acc_value
        avg_accu = sum / iterations
        #print "avg_accu"
        #print avg_accu
        result.append(avg_accu)  
    #print result
    return result


# get_graph will plot the points of the results from get_graph_data and return a graph
def get_graph(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, lower, upper, increment):
    '''
    get_graph - Given a training set, attribute metadata, validation set, numerical splits count, depth, iterations, lower(range),
    upper(range), and increment, this function will graph the results from get_graph_data in reference to the drange
    percentages of the data.
    '''
    step = int((upper - lower) / increment)
    results = []
    pcts = []
    for i in range(step):
        pct = lower + (i + 1) * increment
        pcts.append(pct)
    #print pcts
    results = get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, iterations, pcts)
    print results
    plt.plot(pcts, results)
    plt.show()



