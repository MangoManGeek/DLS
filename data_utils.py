#! /usr/bin/env python3
# -*- coding:utf-8 -*-
############################################################################################################################################################
####### This part of data processing source code is based on [DevinZ1993](https://github.com/DevinZ1993/Chinese-Poetry-Generation)'s implementation. #######
############################################################################################################################################################

from char_dict import end_of_sentence, start_of_sentence
from paths import gen_data_path, plan_data_path, check_uptodate
from poems import Poems
from rank_words import RankedWords
from segment import Segmenter


def gen_train_data():
    print("Generating training data ...")
    segmenter = Segmenter()
    poems = Poems()
    poems.shuffle()
    ranked_words = RankedWords()
    plan_data = []
    gen_data = []
    for poem in poems:
        if len(poem) != 4:
            continue  # Only consider quatrains.
        valid = True
        context = start_of_sentence()
        gen_lines = []
        keywords = []
        for sentence in poem:
            if len(sentence) != 7:
                #只考虑七字诀句
                valid = False
                break
            #get a list of selected words from this sentence
            #ignore all words if they are not in the ranked words list
            words = list(filter(lambda seg: seg in ranked_words,
                                segmenter.segment(sentence)))
            if len(words) == 0:
                valid = False
                break
            keyword = words[0]

            # from all words in this sentence, get the word with highest text_rank score
            for word in words[1:]:
                if ranked_words.get_rank(word) < ranked_words.get_rank(keyword):
                    keyword = word

            gen_line = sentence + end_of_sentence() + \
                       '\t' + keyword + '\t' + context + '\n'
            gen_lines.append(gen_line)
            keywords.append(keyword)
            context += sentence + end_of_sentence()
        if valid:
            # plan data: each line is four keywords from the 4 sentences
            plan_data.append('\t'.join(keywords) + '\n')
            gen_data.extend(gen_lines)
    with open(plan_data_path, 'w') as fout:
        for line in plan_data:
            fout.write(line)
    with open(gen_data_path, 'w') as fout:
        for line in gen_data:
            fout.write(line)


def batch_train_data(batch_size):
    """ Training data generator for the poem generator."""
    gen_train_data()  # Shuffle data order and cool down CPU.
    keywords = []
    contexts = []
    sentences = []
    with open(gen_data_path, 'r') as fin:
        for line in fin.readlines():
            toks = line.strip().split('\t')
            sentences.append(toks[0])
            keywords.append(toks[1])
            contexts.append(toks[2])
            if len(keywords) == batch_size:
                yield keywords, contexts, sentences
                keywords.clear()
                contexts.clear()
                sentences.clear()
        # For simplicity, only return full batches for now.


if __name__ == '__main__':
    if not check_uptodate(plan_data_path) or \
            not check_uptodate(gen_data_path):
        gen_train_data()

    # print(ord('\u6708'))
