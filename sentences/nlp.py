from typing import List, Tuple

import spacy
from spacy.lang.en import English

from .models import Sentence

nlp = spacy.load("en_core_web_lg")


def split_to_sentences(text: str) -> List[str]:
    eng_nlp = English()
    eng_nlp.add_pipe(eng_nlp.create_pipe('sentencizer'))
    doc = eng_nlp(text)
    sentences = [sent.string.strip() for sent in doc.sents]
    return sentences


class SimilarResult:
    def __init__(self, similarity: float, sentence: Sentence):
        self.similarity = similarity
        self.sentence = sentence


def find_similar(source: Sentence, others: List[Sentence]) -> List[SimilarResult]:
    similarity_results = [] # List[SimilarResult]
    for sentence in others:
        similarity = get_similarity(source.content, sentence.content)
        similarity_results.append(SimilarResult(similarity, sentence))

    similarity_results = sorted(similarity_results, key=lambda s: s.similarity, reverse=True)
    return similarity_results


def get_similarity(sentence1: str, sentence2: str) -> float:
    doc1 = nlp(sentence1)
    doc2 = nlp(sentence2)
    similarity = doc1.similarity(doc2)
    return similarity


