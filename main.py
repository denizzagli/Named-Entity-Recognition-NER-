# The libraries I use in this assignment are below.

import math


class Assignment2:

    # Preprocces are made at this stage. The gaps in the dataset have been cleared. 2d array was created with the words "Docstart".

    def preprocess(lines):
        lines.pop(0)
        sentences = []
        sentences_temp = []
        for item in lines:
            list_temp = item.split(' ')
            if list_temp[0] != "-DOCSTART-":
                list_temp[0] = list_temp[0].lower()
                str_temp = ""
                for item in list_temp:
                    str_temp = str_temp + item + ' '
                str_temp = str_temp[:-1]
                sentences_temp.append(str_temp)
            else:
                sentences.append(sentences_temp)
                sentences_temp = []
        if len(sentences_temp) != 0:
            sentences.append(sentences_temp)
        return sentences

    # The number of words forming the denominator in the smoothing process is calculated with this function.

    def find_count_of_unique_words(sentences):
        words = set([])
        for index in range(0, len(sentences)):
            for index2 in range(0, len(sentences[index])):
                list_temp = sentences[index][index2].split(' ')
                words.add(list_temp[0])
        result = len(words)
        return result

    # Initial, transition, emission values are created with this function. The denominators required for smoothing are also
    # created with this function. The frequencies of the Initial, transition, emission values were calculated first. Then
    # the logarithms of the probability values on the basis of 2 were calculated.

    def HMM_Model(sentences, count_of_unique_words):
        initial_temp = {}
        initial = {}
        transition_temp = {}
        transition = {}
        emission_temp = {}
        emission = {}
        for index in range(0, len(sentences)):
            for index2 in range(0, len(sentences[index])):
                list_temp = sentences[index][index2].split(' ')
                if list_temp[-1] not in list(initial_temp.keys()):
                    initial_temp[list_temp[-1]] = 1
                if list_temp[-1] in list(initial_temp.keys()):
                    initial_temp[list_temp[-1]] = initial_temp[list_temp[-1]] + 1
                if index2 != len(sentences[index]) - 1:
                    list_temp2 = sentences[index][index2 + 1].split(' ')
                    str_temp = list_temp[-1]
                    str_temp2 = list_temp2[-1]
                    str_temp3 = str_temp2 + "|" + str_temp
                    if str_temp3 not in list(transition_temp.keys()):
                        transition_temp[str_temp3] = 1
                    if str_temp3 in list(transition_temp.keys()):
                        transition_temp[str_temp3] = transition_temp[str_temp3] + 1
                str_temp = list_temp[0]
                str_temp2 = list_temp[-1]
                str_temp3 = str_temp + "|" + str_temp2
                if str_temp3 not in list(emission_temp.keys()):
                    emission_temp[str_temp3] = 1
                if str_temp3 in list(emission_temp.keys()):
                    emission_temp[str_temp3] = emission_temp[str_temp3] + 1
        initial_sum = sum(list(initial_temp.values()))
        for item in list(initial_temp.keys()):
            initial[item] = math.log2((initial_temp[item] + 1) / (initial_sum + count_of_unique_words))
        transition_sum = sum(list(transition_temp.values()))
        for item in list(transition_temp.keys()):
            transition[item] = math.log2((transition_temp[item] + 1) / (transition_sum + count_of_unique_words))
        emission_sum = sum(list(emission_temp.values()))
        for item in list(emission_temp.keys()):
            emission[item] = math.log2((emission_temp[item] + 1) / (emission_sum + count_of_unique_words))
        initial_smoothing = (initial_sum + len(initial_temp))
        transition_smoothing = (transition_sum + len(transition_temp))
        emission_smoothing = (emission_sum + len(emission_temp))
        return initial, transition, emission, initial_smoothing, transition_smoothing, emission_smoothing

    # Viterbi algorithm, in which word tags are created, is used in this function. As a result, it returns the tags.

    def viterbi_algorithm(sentences, initial, transition, emission, initial_smoothing, transition_smoothing, emission_smoothing):
        emission_keys = list(emission.keys())
        initial_keys = list(initial.keys())
        transition_keys = list(transition.keys())
        all_tags = []
        for index in range(0, len(sentences)):
            initial_state = 0
            tags = []
            for index2 in range(0, len(sentences[index])):
                list_temp = sentences[index][index2].split(' ')
                word = list_temp[0]
                before_tag = ""
                if initial_state == 0:
                    list_temp2 = []
                    for key in initial_keys:
                        prob = 0
                        str_temp = word + '|' + key
                        if str_temp not in emission_keys:
                            int_temp = math.log2(1 / (emission_smoothing))
                            prob = int_temp + initial[key]
                        if str_temp in emission_keys:
                            prob = emission[str_temp] + initial[key]
                        list_temp2.append(prob)
                    max_index = list_temp2.index(max(list_temp2))
                    tag = initial_keys[max_index]
                    tags.append(tag)
                    before_tag = tag
                    initial_state = 1
                else:
                    list_temp2 = []
                    for key in initial_keys:
                        prob = 0
                        str_temp = word + '|' + key
                        str_temp2 = key + '|' + before_tag
                        if str_temp not in emission_keys and str_temp2 not in transition_keys:
                            prob = math.log2(1 / (emission_smoothing)) + math.log2(1 / (transition_smoothing))
                        if str_temp in emission_keys and str_temp2 not in transition_keys:
                            prob = emission[str_temp] + math.log2(1 / (transition_smoothing))
                        if str_temp not in emission_keys and str_temp2 in transition_keys:
                            prob = math.log2(1 / (emission_smoothing)) + transition[str_temp2]
                        if str_temp in emission_keys and str_temp2 in transition_keys:
                            prob = emission[str_temp] + transition[str_temp2]
                        list_temp2.append(prob)
                    max_index = list_temp2.index(max(list_temp2))
                    tag = initial_keys[max_index]
                    tags.append(tag)
                    before_tag = tag
            all_tags.append(tags)
        return all_tags

    # File reading operations were performed in this function.

    def dataset(folderpath):
        input_file = open(folderpath, "r")
        lines = []
        for line in input_file.readlines():
            line = line.strip("\n")
            line_temp = line.split(' ')
            if len(line) != 0 or line_temp[0]:
                lines.append(line)
        return lines

    # It works on the test file and returns the result of how much the code tagged correctly.

    def accuracy(gold_sequence, predicted_sequence):
        correct_words = 0
        all_words = 0
        for index in range(0, len(gold_sequence)):
            for index2 in range(0, len(gold_sequence[index])):
                list_temp = gold_sequence[index][index2].split(' ')
                all_words = all_words + 1
                if list_temp[-1] == predicted_sequence[index][index2]:
                    print(list_temp[-1], predicted_sequence[index][index2])
                    correct_words = correct_words + 1
        result = correct_words / all_words
        return result

NER = Assignment2()

lines = NER.dataset("train.txt")
sentences = NER.preprocess(lines)
count_of_unique_words = NER.find_count_of_unique_words(sentences)
initial, transition, emission, initial_smoothing, transition_smoothing, emission_smoothing = NER.HMM_Model(sentences, count_of_unique_words)

lines2 = NER.dataset("test.txt")
sentences2 = NER.preprocess(lines2)
tags = NER.viterbi_algorithm(sentences2, initial, transition, emission, initial_smoothing, transition_smoothing, emission_smoothing)

# Result -> %85

result = NER.accuracy(sentences2, tags)
