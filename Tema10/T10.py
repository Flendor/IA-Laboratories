import re
from gensim.models import Word2Vec
import numpy as np
# from sklearn import tree
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


def parse_data():
    data = []
    expr = re.compile('\"(.*)\"\\W*,\\W*(\\d)')
    with open('dataset.csv', 'r') as fd:
        lines = fd.readlines()
        for line in lines:
            elements = re.search(expr, line)
            if elements is not None:
                data.append((elements.group(1), elements.group(2)))
    return data


def create_model():
    words_from_sentences = []
    data = parse_data()
    sentences = [data[i][0] for i in range(len(data))]
    expr = re.compile('[\w|\']+')
    for sentence in sentences:
        words = list(map(lambda x: x.lower(), re.findall(expr, sentence)))
        words_from_sentences.append(words)
    model = Word2Vec(words_from_sentences)
    model.save('dataset.model')


def load_model():
    model = Word2Vec.load('dataset.model')
    return model


def point_a(must_create_model=True):
    if must_create_model:
        create_model()
    model = load_model()
    ten_words = ['first', 'movie', 'screen', 'privilege', 'people', 'scenes', 'comedy', 'episodes', 'laugh', 'right']
    for word in ten_words:
        print(word)
        print(model.wv.most_similar(word))


point_a(must_create_model=False)


def get_sets():
    data = parse_data()
    np.random.shuffle(data)
    training_set = data[:int(0.8 * len(data))]
    test_set = data[int(0.8 * len(data)):]
    return training_set, test_set


def train(training_set):
    # separate inputs and labels from the training set
    sentences = [training_set[i][0] for i in range(len(training_set))]
    labels = [training_set[i][1] for i in range(len(training_set))]

    # transform in embedded words (vectors)
    count_vect = CountVectorizer()
    sentences_counts = count_vect.fit_transform(sentences)

    # fit the Word2Vec of this library
    tfidf_transformer = TfidfTransformer()
    sentences_tf = tfidf_transformer.fit_transform(sentences_counts)

    # fit the ML classifier (naive Bayes)
    return MultinomialNB().fit(sentences_tf, labels), count_vect, tfidf_transformer


def test(test_set, classifier, count_vect, tfidf_transformer):
    # separate inputs and labels from the training set
    sentences = [test_set[i][0] for i in range(len(test_set))]
    labels = [test_set[i][1] for i in range(len(test_set))]

    # transform in embedded words (vectors)
    sentences_counts = count_vect.transform(sentences)

    # fit the Word2Vec of this library
    # tfidf_transformer = TfidfTransformer()
    sentences_tfid = tfidf_transformer.transform(sentences_counts)

    predicted = classifier.predict(sentences_tfid)

    misclassified = 0
    for i in range(len(predicted)):
        if predicted[i] != labels[i]:
            misclassified += 1

    print(f"Acc: {(1 - misclassified / len(predicted)) * 100}%.")


sets = get_sets()
classifier, count_vect, tfidf_transformer = train(sets[0])
print()
test(sets[1], classifier, count_vect, tfidf_transformer)
