#! python3
# coding=utf-8


import WordsSplitJIEBAUtils


type_jieba = 0


class WordsSplitHandler:

    def __init__(self, data, analyse_type=type_jieba):
        self.data = data
        self.analyse_type = analyse_type
        if analyse_type == type_jieba:
            self.words_splitter = WordsSplitJIEBAUtils.WordsSplitJIEBAHandler(data)
        self.word_list = None

    def get_split_words(self):
        self.word_list = self.words_splitter.get_split_words()
        return self.word_list

    def simplify(self):
        ret = list()
        if self.word_list is not None:
            for word in self.word_list:
                if word not in ret:
                    ret.append(word)
        return ret
