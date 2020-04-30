from django.db import models

from .nlp import NLProcessor


class Text(models.Model):
    created_at = models.DateTimeField('Created At', auto_now_add=True)
    title = models.CharField('Text Title', max_length=200)

    def __str__(self):
        if not hasattr(self, '_cached_str_'):
            self._cached_str_ = f'{self.title} ({self.sentences.count()-1} sentences)'
        return self._cached_str_

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def parse_and_create(cls, **kwargs):
        text = cls.objects.create(title=kwargs['title'])
        text.save()
        Sentence.create_from_text(text, kwargs['content'])

        return text


class Sentence(models.Model):
    number = models.IntegerField('Sentence number in text')
    content = models.TextField('Sentence text')
    text = models.ForeignKey(Text, related_name='sentences', on_delete=models.CASCADE)
    nlp_doc_bytes = models.BinaryField('Sentence NLP data dump', max_length=2**16)

    class Meta:
        ordering = ['number']
        unique_together = ['number', 'text']

    @classmethod
    def create_from_text(cls, text: Text, content: str):
        """Splits text content into sentences, calculates sentence nlp doc and saves"""
        nlp_processor = NLProcessor()
        text_sentences = nlp_processor.split_to_sentences(content)
        order = 1
        for sentence_content in text_sentences:
            nlp_doc = nlp_processor.get_text_nlp_doc(sentence_content)
            sentence = Sentence.objects.create(
                number=order,
                content=sentence_content,
                text=text,
                nlp_doc_bytes=nlp_doc.to_bytes()
            )
            sentence.save()
            order += 1

    @classmethod
    def find(cls, text_pk, sentence_pk):
        """Finds sentence by pk and parent text pk. Raises Text.DoesNotExist, Sentence.DoesNotExist."""
        text = Text.objects.get(pk=text_pk)
        sentence = Sentence.objects.prefetch_related('text').get(pk=sentence_pk)
        if sentence.text.id != text.id:
            raise cls.DoesNotExist()
        return sentence, text
