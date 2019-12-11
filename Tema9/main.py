import re
import nltk.corpus.reader.wordnet
# punctul a
from nltk.corpus import wordnet


def get_maximum_distance_in_sentence(sentence):
    max_distance = None
    words = re.findall("([A-Z]?[a-z]*)", sentence)
    if words:
        words = set(filter(lambda w: len(w) > 0, words))
        for word in words:
            other_words = words.copy()
            other_words.remove(word)
            distance = get_maximum_distance(word, other_words)
            distance = distance if distance is not None else 0
            if max_distance is None:
                max_distance = distance
            elif max_distance < distance:
                max_distance = distance
        return max_distance
    return 0


def get_maximum_distance(word, words):
    syns = wordnet.synsets(word)
    if len(syns) > 0:
        syns = syns[0]
        max_distance = None
        for other_word in words:
            other_syns = wordnet.synsets(other_word)
            if len(other_syns) > 0:
                other_syns = other_syns[0]
                distance = syns.shortest_path_distance(other_syns)
                distance = distance if distance is not None else 0
                if max_distance is None:
                    max_distance = distance
                elif max_distance < distance:
                    max_distance = distance
        return max_distance
    return None


def get_first_hypernym(word):
    syns = wordnet.synsets(word)
    if len(syns) > 0:
        hypernyms = syns[0].hypernyms()
        if len(hypernyms) > 0:
            return re.sub("_", " ", syns[0].hypernyms()[0].name().split('.', 1)[0])
    return None


def get_first_noun_hypernym(word):
    syns = wordnet.synsets(word)
    if len(syns) > 0:
        for stuff in syns:
            what_is_it = stuff.name().split('.', 2)[1]
            if what_is_it == 'n':
                hypernyms = stuff.hypernyms()
                if len(hypernyms) > 0:
                    return stuff.hypernyms()[0]
    return None


def get_first_lemmas(hypernym):
    lemmas = hypernym.lemmas()
    if len(lemmas) > 0:
        return re.sub("_", " ", hypernym.lemmas()[0].name().split('.', 1)[0])


text = ""
with open("text.txt", "r") as file:
    text = file.read()
    # d
    input_sentences = re.findall(r'([A-Z][^.!?]*[.!?])', text)

    if input_sentences:
        input_sentences = list(filter(lambda w: len(w) > 0, input_sentences))
        for sentence in input_sentences:
            distance = get_maximum_distance_in_sentence(sentence)
            text = re.sub(sentence, sentence + "(" + str(distance) + ")", text)

    input_words = re.findall("([A-Z]?[a-z]*)", text)
    if input_words:
        input_words = set(filter(lambda w: len(w) > 0, input_words))
        for word in input_words:
            # punctul b
            print(get_first_hypernym(word))
            # punctul c
            noun_hypernym = get_first_noun_hypernym(word)
            if noun_hypernym is not None:
                text = re.sub(word, get_first_lemmas(noun_hypernym), text)

with open("text.txt", "w") as file:
    file.write(text)
