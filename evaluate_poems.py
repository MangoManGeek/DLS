from plan import Planner
from rank_words import RankedWords
from poems import Poems
from generateModel import GenerateModel
from paths import data_sxhy_path

import jieba
import csv

"""
evaluate generated scores based on similarity with existing poem dataset NOT Rhyme and Tone
"""

ranked_words = RankedWords()
word_scores = dict()
for pair in ranked_words.word_scores:
    word_scores[pair[0]] = pair[1]


def eval_poems(poem, sorted_poem_scores1, sorted_poem_scores2, sorted_poem_scores3):
    rv_score = 0.0

    # process first lien
    target_score = get_score(poem[0])
    target_poem = binarySearch(sorted_poem_scores, target_score, 1)
    rv_score += abs(target_poem.score2 - target_score)

    # process 2 lien
    target_score = get_score(poem[1])
    target_poem = binarySearch(sorted_poem_scores, target_score, 2)
    rv_score += abs(target_poem.score3 - target_score)

    target_score = get_score(poem[2])
    target_poem = binarySearch(sorted_poem_scores, target_score, 3)
    rv_score += abs(target_poem.score4 - target_score)

    return rv_score


def binarySearch(sorted_poem_scores, target_score, num_of_sentence):
    def get_sentence_score(poem_score, num_of_sentence):

        if num_of_sentence == 1:

            return poem_score.score1

        elif num_of_sentence == 2:

            return poem_score.score2

        elif num_of_sentence == 3:

            return poem_score.score3

        else:

            return poem_score.score4

    l = 0
    r = len(sorted_poem_scores) - 1

    while (l + 1 < r):

        mid = (l + r) // 2

        if (get_sentence_score(sorted_poem_scores[mid], num_of_sentence) < target_score):

            l = mid


        elif (get_sentence_score(sorted_poem_scores[mid], num_of_sentence) > target_score):

            r = mid

        else:

            return sorted_poem_scores[mid]

    if (abs(get_sentence_score(sorted_poem_scores[l], num_of_sentence) - target_score) > abs(
            get_sentence_score(sorted_poem_scores[r], num_of_sentence) - target_score)):
        return sorted_poem_scores[r]
    else:
        return sorted_poem_scores[l]


class PoemScore:

    def __init__(self, sentences):
        self.first = sentences[0]
        self.second = sentences[1]
        self.third = sentences[2]
        self.fourth = sentences[3]

        self.score1, self.keyword1 = get_score(self.first)
        self.score2, self.keyword2 = get_score(self.second)
        self.score3, self.keyword3 = get_score(self.third)
        self.score4, self.keyword4 = get_score(self.fourth)


def get_poem_scores():
    poems = Poems()
    poem_scores = []
    # count=0
    for p in poems:
        # count+=1
        # if count>100:
        # break

        if len(p) != 4:
            continue
        """
        first.append( (get_score(p[0]), p[0]) )
        second.append( (get_score(p[1]), p[0]) )
        third.append( (get_score(p[2]), p[0]) )
        fourth.append( (get_score(p[3]), p[0]) )
        """
        poem_scores.append(PoemScore(p))

    return poem_scores


def get_score(sentence):
    planner = Planner()
    highest_ranked_word = ''
    highest_ranked_score = 0.0

    for word in jieba.lcut(sentence):
        if word not in word_scores:
            continue
        if word_scores[word] > highest_ranked_score:
            highest_ranked_word = word

    # print("keyword is {w}".format(w=highest_ranked_word))
    keyword = set()
    keyword.add(highest_ranked_word)
    score = 0.0
    count = 0

    for word in planner._expand(keyword):
        if word in word_scores:
            score += word_scores[word]
            count += 1
        # else:
            # print('{w} does not have a score'.format(w=word))

    return score / count, highest_ranked_word


def main():
    #planner = Planner()
    #generator = GenerateModel(False)

    poem_scores = get_poem_scores()
    sorted_poem_scores1 = sorted(poem_scores, key=lambda curr_poem: curr_poem.score1)
    sorted_poem_scores2 = sorted(poem_scores, key=lambda curr_poem: curr_poem.score2)
    sorted_poem_scores3 = sorted(poem_scores, key=lambda curr_poem: curr_poem.score3)

    keyword_sorted_poem_scores_table1={}
    for ps in sorted_poem_scores1:
        keyword=ps.keyword1
        if keyword in keyword_sorted_poem_scores_table1:
            keyword_sorted_poem_scores_table1[keyword].append(ps)
        else:
            keyword_sorted_poem_scores_table1[keyword]=[]
            keyword_sorted_poem_scores_table1[keyword].append(ps)

    keyword_sorted_poem_scores_table2={}
    for ps in sorted_poem_scores2:
        keyword=ps.keyword2
        if keyword in keyword_sorted_poem_scores_table2:
            keyword_sorted_poem_scores_table2[keyword].append(ps)
        else:
            keyword_sorted_poem_scores_table2[keyword]=[]
            keyword_sorted_poem_scores_table2[keyword].append(ps)

    keyword_sorted_poem_scores_table3={}
    for ps in sorted_poem_scores3:
        keyword=ps.keyword3
        if keyword in keyword_sorted_poem_scores_table3:
            keyword_sorted_poem_scores_table3[keyword].append(ps)
        else:
            keyword_sorted_poem_scores_table3[keyword]=[]
            keyword_sorted_poem_scores_table3[keyword].append(ps)
    poem=['床前明月光','疑是地上霜','举头望明月','低头思故乡']
    score = eval_poems(poem, keyword_sorted_poem_scores_table1['明月'],\
         keyword_sorted_poem_scores_table2['地上'], keyword_sorted_poem_scores_table3['故乡'])
    print (score)
'''
    avg_score = 0
    num = 500

    for line in open(data_sxhy_path):
        listWords = line.split()
    for i in range(num):
        keyword = listWords[i]
        keywords = planner.plan(keyword)
        poem = generator.generate(keywords)
        #score = eval_poems(poem, sorted_poem_scores1, sorted_poem_scores2, sorted_poem_scores3)
        score = eval_poems(poem, keyword_sorted_poem_scores_table1[keywords[0]],\
         keyword_sorted_poem_scores_table2[keywords[1]], keyword_sorted_poem_scores_table3[keywords[2]])
        avg_score += score
        for sentence in poem:
            print(sentence)


        print("The score of the current poem is:" + score)
    print("The average score is:" + avg_score / num)
    '''



if __name__ == '__main__':
    main()
