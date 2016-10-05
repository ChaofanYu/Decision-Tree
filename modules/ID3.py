import math
from node import Node
import sys
import numpy as np
import operator
import copy

def helper(data_set, attribute_metadata, numerical_splits_count, depth):
    if depth <= 0:
        if len(data_set) >= 1:
            default = majority(data_set)
            node = Node()
            node.label = default
            return node
        else:
            node = Node()
            node.label = 0
            return node
    else:
        depth -= 1
        label_set = []
        data = []
        #print data_set
        for i in data_set:
            label_set.append(i[0])
        #print label_set
        
        labels = [[] for i in range(len(label_set))]
        for i in range(len(label_set)):
            labels[i].append(label_set[i])
        #print labels
        if(len(labels) == 0):
            node = Node()
            node.label = 0
            return node
        elif (len(labels) == 1 or (len(attribute_metadata) - 1) <= 0):
            #print data_set
            default = majority(data_set)
            result = Node()
            result.label = default
            #print result.label
            return result
        elif (check_homogenous(labels)):
            default = label_set[0]
            result = Node()
            result.label = default
            #print result.label
            return result
            #print default
            #return default
        else:
            best = pick_best_attribute(data_set, attribute_metadata, numerical_splits_count)
            #print best
            tree = Node()
            tree.decision_attribute = best[0]
            if (best[1] == "False"): 
                tree.is_nominal = 1
            else: 
                tree.is_nominal = 0
                tree.splitting_value = best[1]
            tree.name = attribute_metadata[best[0]]
            #print tree.name
            tree.label = None

            subset1 = []
            subset2 = []
            result = []

            if(best[1] == "False"):
                result = split_on_nominal(data_set, best[0])
                subset = []
                for i in result.keys():
                    subset = result[i]
                    new_attribute = attribute_metadata[:]
                    new_attribute.pop(best[0])
                    subtree = helper(subset, new_attribute, numerical_splits_count, depth)
                    subtree.results = subset
                    #tree.children[i] = subtree
                return tree
            elif(best[1] != "False"):
                result = split_on_numerical(data_set, best[0], best[1])
                numerical_splits_count[best[0]] -= 1
                subset1 = result[0]
                subset2 = result[1]
                #print subset1 
                #print subset2
                #print attribute_metadata
                new_attribute = attribute_metadata
                #new_attribute.remove(attribute_metadata[best[0]])
                #print new_attribute
                sub1 = helper(subset1, new_attribute, numerical_splits_count[0:], depth)
                sub1.results = subset1
                sub2 = helper(subset2, new_attribute, numerical_splits_count[0:], depth)
                sub2.results = subset2
                tree.children[1] = sub1
                tree.children[2] = sub2
                #print tree.children
                return tree

def ID3(data_set, attribute_metadata, numerical_splits_count, depth):
 

    data_set_copy = data_set
    data_avg = []
    for i in range(len(data_set_copy[0])):
        sum = 0.0
        for j in range(len(data_set_copy)):
            if data_set_copy[j][i] != None:
                #print data_set_copy[j][i]
                sum = sum + data_set_copy[j][i]
            else: sum = sum
        avg = sum / len(data_set_copy)
        if (data_set_copy[1][i] == 1 or data_set_copy[1][i] == 0):
            if avg > 0.5: data_avg.append(1)
            else: data_avg.append(0)
        else: data_avg.append(avg)



    for i in range(len(data_set_copy)):
        for j in range(len(data_set_copy[0])):
            if (data_set_copy[i][j] == None) and (data_set_copy[i - 1][j] != 0 and data_set_copy[i - 1][j] != 1): 
                data_set_copy[i][j] = data_avg[j]
            else:
                if data_set_copy[i][j] == None:
                    data_set_copy[i][j] = data_avg[j]
    return helper(data_set, attribute_metadata, numerical_splits_count, depth)



def majority(data_set):
    labels = []
    for i in data_set:
        if i[0] != '?':
            labels.append(i[0])
    #print labels
    count = {}
    for vote in labels:
        if vote not in count.keys(): count[vote] = 0
        count[vote] += 1
    sortedcount = sorted(count.iteritems(), key = operator.itemgetter(1), reverse = True)
    return sortedcount[0][0] 



def check_homogenous(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Checks if the attribute at index 0 is the same for the data_set, if so return output otherwise None.
    ========================================================================================================
    Output: Return either the homogenous attribute or None
    ========================================================================================================
    '''
    # Your code here
    val = data_set[0]
    for i in data_set:
        if i != val:
            return None
    return 1
# ======== Test Cases =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  None
# data_set = [[0],[1],[None],[0]]
# check_homogenous(data_set) ==  None
# data_set = [[1],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  1

def pick_best_attribute(data_set, attribute_metadata, numerical_splits_count):
    '''
    ========================================================================================================
    Input:  A data_set, attribute_metadata, splits counts for numeric
    ========================================================================================================
    Job:    Find the attribute that maximizes the gain ratio. If attribute is numeric return best split value.
            If nominal, then split value is False.
            If gain ratio of all the attributes is 0, then return False, False
            Only consider numeric splits for which numerical_splits_count is greater than zero
    ========================================================================================================
    Output: best attribute, split value if numeric
    ========================================================================================================
    '''

    gain_ratio = 0.0
    max_gain_ratio = 0.0
    best_attribute = 0
    split_value = 0.0
    final_split_value = 0.0
    for i in xrange(1,len(attribute_metadata)):
        if attribute_metadata[i].values()[0]:      # the attribute is nominal
            gain_ratio = gain_ratio_nominal(data_set,i)
        else:                                      # the attribute is numeric
            if numerical_splits_count[i] > 0:
                gain_ratio_result = gain_ratio_numeric(data_set,i,1)
                gain_ratio = gain_ratio_result[0]
                split_value = gain_ratio_result[1]
            else:
                gain_ratio = 0.0
        if gain_ratio > max_gain_ratio:
                best_attribute = i
                max_gain_ratio = gain_ratio
                final_split_value = split_value
    if max_gain_ratio == 0.0:
        return (False, False)
    if attribute_metadata[best_attribute].values()[0]:
        #print (best_attribute,False)
        return (best_attribute,False)
    else:
        #print (best_attribute, final_split_value)
        return (best_attribute, final_split_value)



# # ======== Test Cases =============================
# numerical_splits_count = [20,20]
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
# data_set = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [0, 0.51], [1, 0.4]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, 0.51)
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "weather",'is_nominal': True}]
# data_set = [[0, 0], [1, 0], [0, 2], [0, 2], [0, 3], [1, 1], [0, 4], [0, 2], [1, 2], [1, 5]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, False)

# Uses gain_ratio_nominal or gain_ratio_numeric to calculate gain ratio.

def mode(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Takes a data_set and finds mode of index 0.
    ========================================================================================================
    Output: mode of index 0.
    ========================================================================================================
    '''
    # Your code here
    count = 0
    for a in data_set:
        if(a[0] == 0):
            count = count + 1;
    if(count == 1):
        return 1
    else:
        return 0
# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# mode(data_set) == 1
# data_set = [[0],[1],[0],[0]]
# mode(data_set) == 0

def entropy(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Calculates the entropy of the attribute at the 0th index, the value we want to predict.
    ========================================================================================================
    Output: Returns entropy. See Textbook for formula
    ========================================================================================================
    '''
    results = {}
    for data in data_set:
        if data[0] not in results:
            results[data[0]] = 0
        results[data[0]] += 1
    ent = 0.0
    #print results
    for val in results.keys():
        p = float(results[val]) / len(data_set)
        ent = ent - p * math.log(p, 2)
    return ent

# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[0],[1],[1],[1]]
# entropy(data_set) == 0.811
# data_set = [[0],[0],[1],[1],[0],[1],[1],[0]]
# entropy(data_set) == 1.0
# data_set = [[0],[0],[0],[0],[0],[0],[0],[0]]
# entropy(data_set) == 0


def gain_ratio_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  Subset of data_set, index for a nominal attribute
    ========================================================================================================
    Job:    Finds the gain ratio of a nominal attribute in relation to the variable we are training on.
    ========================================================================================================
    Output: Returns gain_ratio. See https://en.wikipedia.org/wiki/Information_gain_ratio
    ========================================================================================================
    '''
    # Your code here
    
    labels = [[] for i in range(len(data_set))]
    for data in range(len(data_set)):
        labels[data].append(data_set[data][0])
    #print labels
    results = {}  
    for data in data_set:
        results.setdefault(data[attribute],[]).append(data[0]);
    gain = 0.0
    IV = 0.0
    #print results
    for data in results.keys():
        new = [[] for i in range(len(results.get(data)))]
        #print results.get(data)
        for i in range(len(results.get(data))):
            new[i].append(results.get(data)[i])
        #print new
        #print len(results[data])
        gain += len(results[data]) * entropy(new)
        IV -= float(len(results[data])) / len(data_set) *  math.log((float(len(results[data])) / len(data_set)), 2)
        if(IV == 0.0): IV = 0.1
        #print "IV"
        #print IV
    #print entropy(labels) - gain / len(data_set)
    IG = entropy(labels) - gain / len(data_set)
    #print IV
    ratio = float(IG / IV)
    return ratio



   
# ======== Test case =============================
# data_set, attr = [[1, 2], [1, 0], [1, 0], [0, 2], [0, 2], [0, 0], [1, 3], [0, 4], [0, 3], [1, 1]], 1
# gain_ratio_nominal(data_set,attr) == 0.11470666361703151
# data_set, attr = [[1, 2], [1, 2], [0, 4], [0, 0], [0, 1], [0, 3], [0, 0], [0, 0], [0, 4], [0, 2]], 1
# gain_ratio_nominal(data_set,attr) == 0.2056423328155741
# data_set, attr = [[0, 3], [0, 3], [0, 3], [0, 4], [0, 4], [0, 4], [0, 0], [0, 2], [1, 4], [0, 4]], 1
# gain_ratio_nominal(data_set,attr) == 0.06409559743967516

def gain_ratio_numeric(data_set, attribute, steps):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, and a step size for normalizing the data.
    ========================================================================================================
    Job:    Calculate the gain_ratio_numeric and find the best single threshold value
            The threshold will be used to split examples into two sets
                 those with attribute value GREATER THAN OR EQUAL TO threshold
                 those with attribute value LESS THAN threshold
            Use the equation here: https://en.wikipedia.org/wiki/Information_gain_ratio
            And restrict your search for possible thresholds to examples with array index mod(step) == 0
    ========================================================================================================
    Output: This function returns the gain ratio and threshold value
    ========================================================================================================
    '''
    # Your code here
    
    result = {}
    for x in xrange(0, len(data_set)):
        if x % steps == 0:
            splitnum = split_on_numerical(data_set, attribute, data_set[x][attribute])
            if splitnum[0] == [] or splitnum[1] == []:
                infoRatio = 0
            else:
                left = copy.deepcopy(splitnum[0])
                right = copy.deepcopy(splitnum[1])
                for y in left:
                    y[attribute] = 0
                for y in right:
                    y[attribute] = 1
                new_data_set = left + right
                infoRatio = gain_ratio_nominal(new_data_set, attribute)
            result[infoRatio] = data_set[x][attribute]
    return (max(result.keys()), result[max(result.keys())])
# ======== Test case =============================
# data_set,attr,step = [[1,0.05], [1,0.17], [1,0.64], [0,0.38], [1,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1, 2
# gain_ratio_numeric(data_set,attr,step) == (0.31918053332474033, 0.64)
# data_set,attr,step = [[1, 0.35], [1, 0.24], [0, 0.67], [0, 0.36], [1, 0.94], [1, 0.4], [1, 0.15], [0, 0.1], [1, 0.61], [1, 0.17]], 1, 4
# gain_ratio_numeric(data_set,attr,step) == (0.11689800358692547, 0.94)
# data_set,attr,step = [[1, 0.1], [0, 0.29], [1, 0.03], [0, 0.47], [1, 0.25], [1, 0.12], [1, 0.67], [1, 0.73], [1, 0.85], [1, 0.25]], 1, 1
# gain_ratio_numeric(data_set,attr,step) == (0.23645279766002802, 0.29)

def split_on_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  subset of data set, the index for a nominal attribute.
    ========================================================================================================
    Job:    Creates a dictionary of all values of the attribute.
    ========================================================================================================
    Output: Dictionary of all values pointing to a list of all the data with that attribute
    ========================================================================================================
    '''
    # Your code here
    results = {} 
    for data in data_set:
        val = []
        val.append(data[0])
        val.append(data[1])
        results.setdefault(data[attribute],[]).append(val);
    #result = list(results)
    return results
# ======== Test case =============================
# data_set, attr = [[0, 4], [1, 3], [1, 2], [0, 0], [0, 0], [0, 4], [1, 4], [0, 2], [1, 2], [0, 1]], 1
# split_on_nominal(data_set, attr) == {0: [[0, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3]], 4: [[0, 4], [0, 4], [1, 4]]}
# data_set, attr = [[1, 2], [1, 0], [0, 0], [1, 3], [0, 2], [0, 3], [0, 4], [0, 4], [1, 2], [0, 1]], 1
# split on_nominal(data_set, attr) == {0: [[1, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3], [0, 3]], 4: [[0, 4], [0, 4]]}

def split_on_numerical(data_set, attribute, splitting_value):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, threshold (splitting) value
    ========================================================================================================
    Job:    Splits data_set into a tuple of two lists, the first list contains the examples where the given
	attribute has value less than the splitting value, the second list contains the other examples
    ========================================================================================================
    Output: Tuple of two lists as described above
    ========================================================================================================
    '''
    # Your code here
    tem1 = []
    tem2 = [] 
    for data in data_set:
        if data[1] < splitting_value:
            tem1.append(data)
        else :
            tem2.append(data)
    results = (tem1, tem2)
    #print results
    return results
# ======== Test case =============================
# d_set,a,sval = [[1, 0.25], [1, 0.89], [0, 0.93], [0, 0.48], [1, 0.19], [1, 0.49], [0, 0.6], [0, 0.6], [1, 0.34], [1, 0.19]],1,0.48
# split_on_numerical(d_set,a,sval) == ([[1, 0.25], [1, 0.19], [1, 0.34], [1, 0.19]],[[1, 0.89], [0, 0.93], [0, 0.48], [1, 0.49], [0, 0.6], [0, 0.6]])
# d_set,a,sval = [[0, 0.91], [0, 0.84], [1, 0.82], [1, 0.07], [0, 0.82],[0, 0.59], [0, 0.87], [0, 0.17], [1, 0.05], [1, 0.76]],1,0.17
# split_on_numerical(d_set,a,sval) == ([[1, 0.07], [1, 0.05]],[[0, 0.91],[0, 0.84], [1, 0.82], [0, 0.82], [0, 0.59], [0, 0.87], [0, 0.17], [1, 0.76]])