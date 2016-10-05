from node import Node
from ID3 import *
from operator import xor
from copy import deepcopy

# Note, these functions are provided for your reference.  You will not be graded on their behavior,
# so you can implement them as you choose or not implement them at all if you want to use a different
# architecture for pruning.

def reduced_error_pruning(root,training_set,validation_set):
    '''
    take the a node, training set, and validation set and returns the improved node.
    You can implement this as you choose, but the goal is to remove some nodes such that doing so improves validation accuracy.
    '''
    # Your code here
    head = deepcopy(root)
    accuracy, newtree = pruning(head, training_set, validation_set)
    return accuracy, newtree


def pruning(root, training_set, validation_set):
    '''
    recursive to decide which node to prune
    '''
    accuracy_begin = validation_accuracy(root, validation_set)
    head = deepcopy(root)
    all_node = bfs(head)
    accuracy = []
    for i in range(len(all_node)):
        new_dict = deepcopy(all_node)
        prune_this_node(new_dict[i])
        acc = validation_accuracy(new_dict[0], validation_set)
        accuracy.append(acc)
    max_acc = max(accuracy)
    max_index = accuracy.index(max_acc)
    if max_acc > accuracy_begin:
        prune_this_node(all_node[max_index])
        return pruning(head, training_set, validation_set)
    else:
        return accuracy_begin, root


def prune_this_node(node):
    if node.children is None:
        return
    else:
        count = []
        node_now = [node]
        while node_now:
            node_next = []
            for i in node_now:
                if i is None:
                    continue
                else:
                    if i.label is not None:
                        count.append(i)
                    else:
                        for each in range(len(i.children)):
                            node_next.append(i.children.get(each + 1))
            node_now = node_next
        count_label = []
        for n in count:
            count_label.append([n.label])
        if len(count_label) == 1:
            node.label = count_label[0][0]
        elif len(count_label) > 1:
            node.label = mode(count_label)
        node.children.clear()


def bfs(root):
    thislevel = [root]
    temp = []
    while thislevel:
        nextlevel = []
        for n in thislevel:
            if n is None:
                continue
            else:
                temp.append(n)
                if n.label is None:
                    for i in range(len(n.children)):
                        nextlevel.append(n.children.get(i + 1))
        thislevel = nextlevel
    return temp

def validation_accuracy(tree, validation_set):
    '''
    takes a tree and a validation set and returns the accuracy of the set on the given tree
    '''
    count = 0.0
    for entry in validation_set:
        if tree.classify(entry) == entry[0]:
            count += 1
    return count/len(validation_set) * 100