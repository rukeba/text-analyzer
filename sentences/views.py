from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Text, Sentence
from .serializers import TextSerializer, NewTextSerializer, SimilarSentencesSerializer


@api_view(['GET', 'POST'])
def text_list(request):
    if request.method == 'GET':
        snippets = Text.objects.all()
        serializer = TextSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = NewTextSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def text_detail(request, pk):
    try:
        text = Text.objects.get(pk=pk)
    except Text.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TextSerializer(text)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        text.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def sentence_similar_list(request, text_pk, sentence_pk):
    try:
        text = Text.objects.get(pk=text_pk)
        sentence = Sentence.objects.get(pk=sentence_pk)
        if sentence.text.id != text.id:
            raise Sentence.DoesNotExist()
    except (Text.DoesNotExist, Sentence.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    similar = text.sentences.all()

    serializer = SimilarSentencesSerializer({
        'source': sentence,
        'similar': similar
    })

    return Response(serializer.data)



