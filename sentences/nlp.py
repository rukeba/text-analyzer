from typing import List
import itertools

import spacy
from spacy.tokens import Doc


class NLProcessor(object):

    _nlp = None

    @classmethod
    def get_nlp(cls) -> Doc:
        if not cls._nlp:
            cls._nlp = spacy.load("en_core_web_lg")
        return cls._nlp

    _english = None

    @classmethod
    def get_english(cls):
        if not cls._english:
            from spacy.lang.en import English
            cls._english = English()
            cls._english.add_pipe(cls._english.create_pipe('sentencizer'))
        return cls._english

    @classmethod
    def split_to_sentences(cls, text: str) -> List[str]:
        english = cls.get_english()
        doc = english(text)
        sentences = [sent.string.strip() for sent in doc.sents]
        return sentences

    @classmethod
    def get_text_nlp_doc(cls, text: str):
        nlp = cls.get_nlp()
        doc = nlp(text)
        return doc

    @classmethod
    def load_nlp_doc_from_bytes(cls, dump: bytes):
        nlp = cls.get_nlp()
        doc = Doc(nlp.vocab).from_bytes(dump)
        return doc

    class SimilarSentence:
        def __init__(self, similarity: float, sentence: 'Sentence'):
            self.similarity = similarity
            self.sentence = sentence

        def __repr__(self):
            return f'{self.__class__}(sentence={self.sentence}, similarity={self.similarity})'

    class SimilarText:
        def __init__(self, text: 'Text'):
            self.text = text
            self.similar_sentences = [] # type: List['NLProcessor.SimilarSentence']

        def add_similar_sentence(self, similar_sentence: 'NLProcessor.SimilarSentence'):
            self.similar_sentences.append(similar_sentence)

        def __repr__(self):
            return f'{self.__class__}(text={self.text}, similar_sentences={self.similar_sentences})'

    @classmethod
    def find_similar(cls, source: 'Sentence', others: List['Sentence']) -> List['NLProcessor.SimilarText']:
        all_similar_sentences = [] # List[SimilarResult]
        source_doc = cls.load_nlp_doc_from_bytes(source.nlp_doc_bytes)

        for other in others:
            other_doc = cls.load_nlp_doc_from_bytes(other.nlp_doc_bytes)
            similarity = source_doc.similarity(other_doc)
            all_similar_sentences.append(cls.SimilarSentence(similarity, other))

        # sort similar by score
        all_similar_sentences = sorted(all_similar_sentences, key=lambda s: s.similarity, reverse=True)

        # re-group by texts
        texts = {}
        for sr in all_similar_sentences:
            key = sr.sentence.text.id
            if key in texts:
                texts[key].add_similar_sentence(sr)
            else:
                st = cls.SimilarText(sr.sentence.text)
                st.add_similar_sentence(sr)
                texts[key] = st

        result = list(texts.values())

        print(result)

        return result

