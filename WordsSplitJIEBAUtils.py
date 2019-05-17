#! python3
# coding=utf-8


import jieba


class WordsSplitJIEBAHandler:

    def __init__(self, data):
        self.data = data

    def get_split_words(self):
        word_list = list()
        words = jieba.cut_for_search(self.data)
        for word in words:
            word_list.append(word)
        return word_list
