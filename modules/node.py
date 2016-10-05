# DOCUMENTATION
# =====================================
# Class node attributes:
# ----------------------------
# children - a list of 2 if numeric and a dictionary if nominal.  
#            For numeric, the 0 index holds examples < the splitting_value, the 
#            index holds examples >= the splitting value
#
# label - is None if there is a decision attribute, and is the output label (0 or 1 for
#	the homework data set) if there are no other attributes
#       to split on or the data is homogenous
#
# decision_attribute - the index of the decision attribute being split on
#
# is_nominal - is the decision attribute nominal
#
# value - Ignore (not used, output class if any goes in label)
#
# splitting_value - if numeric, where to split
#
# name - name of the attribute being split on
import numpy as np


class Node:
    def __init__(self):
        # initialize all attributes
        self.label = None
        self.decision_attribute = None
        self.is_nominal = None
        self.value = None
        self.splitting_value = None
        self.children = {}
        self.name = None
        self.results = []
    
    def classify(self, instance):
        '''
        label = 0.5
        #print instance
        if not self:
            return None
        if self.label is not None:
            label = self.label
            #print label
            return label
        if self.is_nominal == True:
            for child in self.children:
                if self.children[child].name == instance[self.decision_attribute]:
                    label = classify(self.child, instance)
        #print label
        else:
            if (instance[self.decision_attribute] < self.splitting_value):
                if self.children[1] == 1 or self.children[1] == 0:
                    return self.children[1]
                else: label = Node.classify(self.children[1], instance)
            else:
                if self.children[2] == 1 or self.children[2] == 0:
                    return self.children[2]
                else: label = Node.classify(self.children[2], instance)
        return label
        '''
        if self.label == 1:
            return 1
        if self.label == 0:
            return 0
        if self.label == None:
            if self.is_nominal == True:
                difference = {}
                for splitval in self.children.keys():
                    if splitval == instance[self.decision_attribute]:
                        return self.children[splitval].classify(instance)
                    else:
                        difference[abs(instance[self.decision_attribute] - splitval)] = splitval
                return self.children[difference[min(difference.keys())]].classify(instance)
            else:
                if instance[self.decision_attribute] < self.splitting_value:
                    #print self.children[1].splitting_value
                    return self.children[1].classify(instance)
                else:
                    #print self.children[2].splitting_value
                    return self.children[2].classify(instance)

    def print_tree(self, indent = 0):
        '''
        returns a string of the entire tree in human readable form
        '''
        # Your code here
        pass



    def print_dnf_tree(self):
        '''
        returns the disjunct normalized form of the tree.
        '''
        print 'The DNF of Tree:\n'
        resList=self.find_dnf()
        res=''
        for i in resList:
            if i != resList[0]:
                res+='v'
            res+='('+i+')'
        print res
        return res
                
        pass
    
    def find_dnf(self):
        resList=[]
        resList1=[]
        rl=[]
        rl2=[]
        if self.label==1:
            return ['True']
        if self.label==0:
            return ['False']
        
        if not self.is_nominal:
            resList=self.children[1].find_dnf()
            if resList[0]=='True':
                rl+=[str(self.name)+'<'+str(self.splitting_value)]
            else:
                if resList[0]=='False':
                    resList=[]
                else:
                    for x in resList:
                        x=str(self.name)+'<'+str(self.splitting_value)+'^'+x
                        rl+=[x]
            resList1=self.children[2].find_dnf()
            if resList1==[]:
                resList1+='False'
            if resList1[0]=='True':
                rl2+=[str(self.name)+'>='+str(self.splitting_value)]
                
            else:
                if resList1[0]=='False':
                    resList1=[]
                else:
                    for x in resList1:
                        x+='^'+str(self.name)+'>='+str(self.splitting_value)
                        rl2+=[x]
            resList=rl+rl2
        else:
            for i in self.children:
                resList1=self.children[i].find_dnf()
                if resList1[0]=='True':
                    rl+=[str(self.name)+'='+str(i)]
                else:
                    if resList1[0]=='False':
                        resList1=[]
                    else:
                        for x in resList1:
                            x+='^'+str(self.name)+'='+str(i)
                            rl+=[x]
                resList+=rl
        return resList