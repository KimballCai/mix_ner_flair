#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
@version:0.1
@author:Cai Qingpeng
@file: test.py
@time: 2020/3/18 7:30 PM
'''


import os
import argparse

def parse_args():
    # parse arguments
    ## general
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--path', default="./log/pool_flair_f_20200330002549/",help='model path')
    arg_parser.add_argument('--gpu', default="0", help='0,1,2')
    return arg_parser.parse_args()

ARGS = parse_args()
os.environ["CUDA_VISIBLE_DEVICES"] = ARGS.gpu

from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.models import SequenceTagger
from eval.conlleval import evaluate

if not os.path.exists(ARGS.path + '/best-model.pt'):
    raise FileNotFoundError(ARGS.path + '/best-model.pt' + " is not exist!")

# define columns
columns = {0: 'text', 1: '_', 2: '_', 3: 'ner'}

# this is the folder in which train, test and dev files reside
data_folder = './data'  # /path/to/data/folder

# init a corpus using column format, data folder and the names of the train, dev and test files
corpus: Corpus = ColumnCorpus(data_folder, columns,
                              train_file='train.txt',
                              test_file='test.txt',
                              dev_file='valid.txt')
print(corpus)

tag_type = 'ner'
tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
print(tag_dictionary)

model = SequenceTagger.load(ARGS.path + '/best-model.pt')

pred = []
real = []

for sentence in corpus.test:
    for token in sentence.tokens:
        real.append(token.get_tag("ner").value)

def model_prediction(model):
    model_pred = []
    for sentence in corpus.test:
        model.predict(sentence)
        for token in sentence.tokens:
            model_pred.append(token.get_tag("ner").value)
    return model_pred

print("****** prediction ******")
mdoel_pred = model_prediction(model)
print(evaluate(real,mdoel_pred))
