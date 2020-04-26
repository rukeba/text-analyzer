import nltk


def split_to_sentences(text: str) -> list:
    sentences = nltk.sent_tokenize(text)
    return sentences
