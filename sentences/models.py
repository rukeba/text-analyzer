from django.db import models

from . import nlp

class Text(models.Model):
    created_at = models.DateTimeField('Created At', auto_now_add=True)
    title = models.CharField('Text Title', max_length=200)

    def __str__(self):
        if not hasattr(self, '_cached_str_'):
            self._cached_str_ = f'{self.title} ({self.sentences.count()-1} sentences)'
        return self._cached_str_

    @classmethod
    def parse_and_create(cls, **kwargs):
        text = cls.objects.create(title=kwargs['title'])
        text.save()
        text_sentences = nlp.split_to_sentences(kwargs['content'])
        order = 0
        for sentence_content in text_sentences:
            sentence = Sentence.objects.create(number=order, content=sentence_content.strip(), text=text)
            sentence.save()
            order += 1

        return text


class Sentence(models.Model):
    number = models.IntegerField('Sentence number in text')
    content = models.TextField('Sentence text')
    text = models.ForeignKey(Text, related_name='sentences', on_delete=models.CASCADE)

    class Meta:
        ordering = ['number']
        unique_together = ['number', 'text']

    @classmethod
    def find(cls, text_pk, sentence_pk):
        """Finds sentence by pk and parent text pk. Raises Text.DoesNotExist, Sentence.DoesNotExist."""
        text = Text.objects.get(pk=text_pk)
        sentence = Sentence.objects.get(pk=sentence_pk)
        if sentence.text.id != text.id:
            raise cls.DoesNotExist()
        return sentence, text
