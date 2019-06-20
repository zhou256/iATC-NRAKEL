# -*- coding: utf-8 -*-

"""
	function ：Metrics of iATC-NRAKEL for multi-label classification.
"""

import numpy as np
import pandas as pd

def load_resultfile(filename):
    with open(filename, 'r+') as fp:
        content = fp.readlines()
    content1 = []
    result_matrix = []
    count = 0
    for line in content[3:3 + 3883]:
        content1.append(line)
    for line in content1:
        count += 1
        strstr1 = line.strip().split('[ ')
        trueLabel = [int(x) for x in strstr1[1].split(' ]')[0].split(' ')]
        predLabel = [1 if (float(x) > 0.5) else 0 for x in strstr1[2].split(' ]')[0].split(' ')]
        result_matrix.append([count, trueLabel, predLabel])
    return result_matrix


def Intersect_set(a, b):
    countL = 0
    for i in range(len(a)):
        if a[i] == 1 and b[i] == 1:
            countL += 1
        else:
            continue
    return countL


def unionset(line1, line2):
    sum2 = 0
    for i in range(len(line1)):
        if (line1[i] == 0 and line2[i] == 1) or (line1[i] == 1 and line2[i] == 0) or (line1[i] == 1 and line2[i] == 1):
            sum2 += 1
    return sum2


def Aiming(preLabels, test_targets, D):
    # molecular
    sumsum1 = 0
    for i in range(D):
        line1, line2 = preLabels[i], test_targets[i]
        # denominator
        line1_count = 0
        for i in range(len(line1)):
            if line1[i] == 1:
                line1_count += 1
        sumsum1 += Intersect_set(line1, line2) / line1_count
    return sumsum1 / D


def Coverage(preLabels, test_targets, D):
    # molecular
    sumsum1 = 0
    for i in range(D):
        line1, line2 = preLabels[i], test_targets[i]
        # denominator
        line2_count = 0
        for i in range(len(line2)):
            if line2[i] == 1:
                line2_count += 1
        sumsum1 += Intersect_set(line1, line2) / line2_count
    return sumsum1 / D


def Abs_True_Rate(preLabels, test_targets, D):
    correct_pairs = 0
    for i in range(len(preLabels)):
        if preLabels[i] == test_targets[i]:
            correct_pairs += 1
    abs_true = correct_pairs / D
    return abs_true


def Abs_False_Rate(preLabels, test_targets, D):
    correct_pairs = 0.0
    for i in range(len(preLabels)):
        line1, line2 = preLabels[i], test_targets[i]
        correct_pairs += (unionset(line1, line2) - Intersect_set(line1, line2)) / 14
    abs_false = correct_pairs / D
    return abs_false


def Accuracy(preLabels, test_targets, D):
    acc_score = 0
    for i in range(len(preLabels)):
        item_inter = Intersect_set(preLabels[i], test_targets[i])
        item_union = unionset(preLabels[i], test_targets[i])
        acc_score += item_inter / item_union
    accuracy = acc_score / D
    return accuracy


if __name__ == '__main__':
    filename = '../data/Metrics/drug3883_multilabel_jackneaf.txt'
    # jackkneaf score
    dfdf11 = pd.DataFrame(columns=['accuracy', 'abs_true_rate', 'Aming', 'abs_false_rate', 'coverage'])
    for i in range(1):
        result_matrix = load_resultfile(filename)
        D = len(result_matrix)  # numbers of samples.
        preLabels = []
        test_targets = []
        for line in result_matrix:
            preLabels.append(line[1])
            test_targets.append(line[2])
        exact_match = Abs_True_Rate(preLabels, test_targets, D)
        accuracy = Accuracy(preLabels, test_targets, D)
        Aming1 = Aiming(preLabels, test_targets, D)
        abs_false = Abs_False_Rate(preLabels, test_targets, D)
        coverage = Coverage(preLabels, test_targets, D)
        print(exact_match,"#",accuracy,"#",Aming1,"#",abs_false,"#",coverage)
        dfdf11.loc[i, 'accuracy'] = np.round(accuracy, 4)
        dfdf11.loc[i, 'abs_true_rate'] = np.round(exact_match, 4)
        dfdf11.loc[i, 'Aming'] = np.round(Aming1, 4)
        dfdf11.loc[i, 'abs_false_rate'] = np.round(abs_false, 4)
        dfdf11.loc[i, 'coverage'] = np.round(coverage, 4)
    dfdf11.to_csv("../data/Metrics/metrics.csv", index=False, header=True)
