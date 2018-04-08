#!/usr/bin/python
# -*- coding: utf-8 -*-

# @File  : model.py
# @Author: JohnHuiWB
# @Date  : 2018/4/5 0005
# @Desc  : 
# @Contact : huiwenbin199822@gmail.com 
# @Software : PyCharm

import numpy as np
from os import path
from keras import Sequential
from MoodFeeler.token import *
from keras.models import load_model
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
from MoodFeeler.data import get_train_data, get_test_data
from keras.layers import Embedding, Bidirectional, GRU, Dense


class Model(object):
    def __init__(self):
        self._dir = path.dirname(path.realpath(__file__))
        self._model_path = path.join(self._dir, 'test_model.h5')
        self._model_png_path = path.join(self._dir, 'model.png')
        self._vocab_len = len(get_tokenizer().word_index)
        self._maxlen = 40
        self._num_labels = 2
        if path.exists(self._model_path):
            print('Loading mood feeler model...')
            self._model = self._load_model()
        else:
            print('Mood feeler model does not exist!!!')
            print('Please use \'train\' method to train a new model.')

    def _get_model(self):
        """
        模型结构：词嵌入-双向GRU*2-全连接
        :return:
        """
        model = Sequential()
        model.add(Embedding(self._vocab_len + 1, 300))
        model.add(Bidirectional(GRU(256, dropout=0.2, recurrent_dropout=0.1, return_sequences=True)))
        model.add(Bidirectional(GRU(256, dropout=0.2, recurrent_dropout=0.1)))
        model.add(Dense(self._num_labels, activation='softmax'))
        model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])
        return model

    def draw_model(self):
        model = self._get_model()
        from keras.utils.vis_utils import plot_model
        # 神经网络可视化
        plot_model(model, to_file=self._model_png_path, show_shapes=True)

    def train(self, batch_size=32, epochs=5):
        # 载入训练集
        df = get_train_data()
        x = []
        y = []
        for _, text, label in df.get_values():
            x.append(text)
            if label == 1:
                y.append([1.0, 0.0])
            elif label == 0:
                y.append([0.0, 1.0])
        y = np.array(y)
        # padding
        x = t2s(x, self._maxlen)
        # 划分train和validation
        x_t, x_v, y_t, y_v = train_test_split(x, y, test_size=0.2, random_state=0)

        model = self._get_model()
        ckpt = ModelCheckpoint(self._model_path, monitor='val_loss', save_best_only=True)
        model.fit(x_t, y_t,
                  batch_size=batch_size,
                  epochs=epochs,
                  validation_data=(x_v, y_v),
                  shuffle=True,
                  callbacks=[ckpt]
                  )

    def _load_model(self):
        return load_model(self._model_path)

    def eval(self):
        test_data = get_test_data()
        x = []
        y = []
        for _, text, label in test_data.get_values():
            x.append(text)
            y.append(label)
        model = self._load_model()

        # 保留原始的texts，以便输出
        from copy import deepcopy
        x_o = deepcopy(x)

        x = t2s(x, self._maxlen)
        TP, FP, TN, FN = 0, 0, 0, 0

        result = model.predict_on_batch(x)

        for i in range(len(y)):
            if y[i] == 1:
                if result[i][0] > result[0][1]:
                    # print('TP:\t', x_o[i])
                    TP += 1
                else:
                    print('FN:\t', x_o[i], '\n\tR:\t', result[i])
                    FN += 1
            else:
                if result[i][0] < result[i][1]:
                    # print('TN:\t', x_o[i])
                    TN += 1
                else:
                    print('FP:\t', x_o[i], '\n\tR:\t', result[i])
                    FP += 1
        print('TP:{}\tFP:{}\tTN:{}\tFN:{}\t'.format(TP, FP, TN, FN))
        p = TN/(TN+FN)
        r = TN/(TN+FP)
        f1 = 2*p*r/(p+r)
        print('Following scores base on negative texts.')
        print('Precision:\t', p)
        print('Recall:\t', r)
        print('F_1 score:\t', f1)

    def predict(self, texts: list):
        x = t2s(texts, self._maxlen)
        return self._model.predict_on_batch(x)
