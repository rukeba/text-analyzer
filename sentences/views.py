from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Text, Sentence
from .serializers import NewTextSerializer, TextSerializer, TextDetailSerializer, SentenceSerializer, SimilarSentenceSerializer
from .nlp import find_similar


def ui(request):
    return render(request, 'index.html')


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
        serializer = TextDetailSerializer(text)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        text.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def sentence_detail(request, text_pk, sentence_pk):
    try:
        sentence, _ = Sentence.find(text_pk, sentence_pk)
    except (Text.DoesNotExist, Sentence.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = SentenceSerializer(sentence)
    return Response(serializer.data)


@api_view(['GET'])
def sentence_similar_list(request, text_pk, sentence_pk):
    try:
        sentence, text = Sentence.find(text_pk, sentence_pk)
    except (Text.DoesNotExist, Sentence.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    other = text.sentences.exclude(pk=sentence.id)
    similar = find_similar(sentence, other)
    serializer = SimilarSentenceSerializer(similar, many=True)
    return Response(serializer.data)



