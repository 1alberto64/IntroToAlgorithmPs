import random
from PyDictionary import PyDictionary
dictionary=PyDictionary()

input = 'Imeetpeoplethere'
# input = 'meetmenow'
# input = 'meetateight'


def quality(word):
    if len(word) <= 1:
        return 1
    meaning = dictionary.meaning(word, 'en')
    if meaning is not None:
        return len(word)*100
    else:
        return 0


def best_segmentation(sentence):
    word_history = dict()

    quality_total, word_list = best_segmentation_helper(sentence, -1, word_history)

    return quality_total, word_list


def best_segmentation_helper(sentence, index, history):
    max_quality_total = -1
    max_word_list = []

    if len(sentence) <= 1:
        max_quality_total = quality(sentence)
        max_word_list = [sentence]
        return max_quality_total, max_word_list

    if index > 0:
        word = sentence[:index]
        word_quality = quality(word)
        rest_of_sentence = sentence[index:]
    else:
        word = None
        word_quality = 0
        rest_of_sentence = sentence[:]

    for index_of_rest in range(1, len(rest_of_sentence)+1):
        if (rest_of_sentence, index_of_rest) in history:
            quality_total, word_list = history[(rest_of_sentence, index_of_rest)]
        else:
            quality_total, word_list = best_segmentation_helper(rest_of_sentence, index_of_rest, history)
            history[(rest_of_sentence, index_of_rest)] = quality_total, word_list[:]

        if quality_total > max_quality_total or max_quality_total < 0:
            max_quality_total = quality_total
            max_word_list = word_list[:]

    if word is not None:
        max_word_list.insert(0, word)
    if max_quality_total < 0:
        max_quality_total = 0
    max_quality_total += word_quality

    history[sentence] = max_quality_total, max_word_list

    return max_quality_total, max_word_list


quality_total, word_list = best_segmentation(input)

print('The word: ', input)
print("The best word list is: ", ', '.join(word_list))
print("The best quality is: ", quality_total)


# T(n) = SUM[1, n-1](T(n-k))