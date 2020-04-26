from django.db import models


class Text(models.Model):
    created_at = models.DateTimeField('Created At', auto_now_add=True)
    title = models.CharField('Text Title', max_length=200)

    def __str__(self):
        if not hasattr(self, '_cached_str_'):
            self._cached_str_ = f'{self.title} ({self.sentences.count()-1} sentences)'
        return self._cached_str_

    @classmethod
    def parse_and_create(cls, **kwargs):
        text = Text.objects.create(title=kwargs['title'])
        text.save()
        text_sentences = kwargs['content'].split('.')
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
