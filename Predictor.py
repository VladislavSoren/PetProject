import  pandas as pd
import numpy as np
import tensorflow as tf

class Model():
    def __init__(self):
        # получаем массив уникальных скилов
        df = pd.read_csv('Data_uniq.csv', index_col=0)
        df = df.astype(int)
        self.uniq_skills = df.columns.values

        # получаем предсказывающую модель
        self.model = tf.keras.models.load_model('Salaries_predictor')

    # метод получения примера для предсказания
    def get_sample(self, custom_skills):
        vector = np.zeros(len(self.uniq_skills))
        for skill in custom_skills:
            for i, u_skill in enumerate(self.uniq_skills):
                if skill == u_skill:
                    vector[i] = 1
        return vector.reshape(1, len(self.uniq_skills))

    # метод получения предсказания
    def get_predict(self, sample):
        predict = self.model.predict(sample)
        return predict
