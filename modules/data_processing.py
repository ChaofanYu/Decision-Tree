from ID3 import *
def data_processing(data_set,attribute_metadata):
    for i in range(1, len(attribute_metadata)):
        if attribute_metadata[i]['is_nominal'] == True:
            subset = []
            for entry in data_set:
                if entry[i] != None:
                    subset.append([entry[i]])
            predict = mode(subset)
            for j in range(0,len(data_set)):
                if data_set[j][i] == None:
                    data_set[j][i] = predict
        else:
            value = 0
            length = 0
            for entry in data_set:
                if entry[i] != None:
                    value = value + entry[i]
                    length += 1
            predict = value/length
            for j in range(0, len(data_set)):
                if data_set[j][i] == None:
                    data_set[j][i] = predict
    return data_set
