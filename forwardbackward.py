import os
import sys
import numpy as np


def run(test, word, tag, prior, emit, trans, predict):
    word_file = open(word, 'r')
    wordIndex = word_file.read().splitlines()
    # print("wordIndex: ", wordIndex)
    tag_file = open(tag, 'r')
    tagIndex = tag_file.read().splitlines()
    # print("tagIndex: ", tagIndex)

    prior_file = open(prior, 'r')
    priorData = prior_file.read().splitlines()
    emit_file = open(emit, 'r')
    emitData = emit_file.read().splitlines()
    trans_file = open(trans, 'r')
    transData = trans_file.read().splitlines()
    test_file = open(test, 'r')
    input = test_file.read().splitlines()

    pi = getArray(priorData)
    # print(pi)
    B = getMatrix(emitData, len(tagIndex), len(wordIndex))
    # print(B)
    A = getMatrix(transData, len(tagIndex), len(tagIndex))
    # print(A)
    testData = getInput(input, wordIndex)
    # print("testData: ", testData)

    output = ""
    for line in testData:
        label = ""
        alpha = getAlpha(line, pi, A, B)
        # print("alpha: ", alpha)
        beta = getBeta(line, pi, A, B)
        # print("beta: ", beta)
        for i in range(len(line)):
            word = wordIndex[line[i]]
            cal = np.multiply(alpha[i], beta[i]).tolist()
            tag_index = cal.index(max(cal))
            tag = tagIndex[tag_index]
            predict_tag = "{}_{} ".format(word, tag)
            label += predict_tag
        output += label
        output += "\n"
    # print(output)

    predict_file = open(predict, 'w')
    predict_file.write(output)

    word_file.close()
    tag_file.close()
    prior_file.close()
    emit_file.close()
    trans_file.close()
    test_file.close()
    predict_file.close()

def getArray(prior):
    res = np.zeros(len(prior))
    for i in range(len(prior)):
        res[i] = float(prior[i])
    return res


def getMatrix(matrix, height, width):
    res = np.zeros((height, width))
    for i in range(height):
        line = matrix[i].split()
        res[i] = getArray(line)
    return res


def getInput(input, words):
    res = []
    for line in input:
        row = []
        cur = line.split()
        for elem in cur:
            pair = elem.split("_")
            num = words.index(pair[0])
            row.append(num)
        res.append(row)
    return res


def getAlpha(line, pi, A, B):
    Alpha = []
    alpha1 = np.multiply(pi, B[:, line[0]])
    Alpha.append(alpha1)
    # print("AT: ", np.transpose(A))
    for i in range(1, len(line)):
        x = line[i]
        # print("------------x: ", x)
        pre = np.transpose(np.matrix(Alpha[-1]))
        # print("pre: ", pre)
        cur_alpha = np.transpose(np.transpose(A) * pre)
        # print("cur_alpha: ", cur_alpha)
        # print("b: ", B[:, x])
        cur = np.multiply(B[:, x], np.squeeze(np.asarray(cur_alpha)))
        # print("cur: ", cur)
        Alpha.append(cur)
    return Alpha


def getBeta(line, pi, A, B):
    Beta = []
    beta1 = np.array([1] * len(pi))
    Beta.append(beta1)
    for i in range(len(line) - 1, 0, -1):
        x = line[i]
        #print("------------x: ", x)
        #print("beta: ", Beta[0])
        #print("b: ", B[:, x])
        cur_beta = np.multiply(B[:, x], Beta[0])
        #print("cur_beta: ", cur_beta)
        cur = A * np.transpose(np.matrix(cur_beta))
        cur = np.transpose(cur)
        Beta.insert(0, np.squeeze(np.asarray(cur)))

    return Beta


if __name__ == '__main__':
    testData = sys.argv[1]
    wordIndex = sys.argv[2]
    tagIndex = sys.argv[3]
    prior = sys.argv[4]
    emit = sys.argv[5]
    trans = sys.argv[6]
    predict = sys.argv[7]

    run(testData, wordIndex, tagIndex, prior, emit, trans, predict)