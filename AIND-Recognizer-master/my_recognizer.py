import warnings
from asl_data import SinglesData
import re

def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # implement the recognizer
    words = test_set.get_all_Xlengths()

    for idx in words:
        word = words[idx][0]
        probability = {}
        for key in models:
            model = models[key]
            try:
                probability[key] = model.score(word)
            except:
                probability[key] = 0

        # print(sum(1 for x in probability.values() if x == 0))
        probabilities.append(probability)
        guess = max(probability, key=probability.get)
        # Like described in the lecture, I consider "GIVE1", "GIVE2" should be same
        # as "GIVE"
        guess = re.sub('\d', '', guess)
        guesses.append(guess)
    return probabilities, guesses
