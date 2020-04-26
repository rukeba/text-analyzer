from rest_framework import serializers
from .models import Text, Sentence


class NewTextSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, allow_blank=False, max_length=200)
    content = serializers.CharField(required=True, allow_blank=False, trim_whitespace=True, max_length=100000, write_only=True)

    def create(self, validated_data):
        return Text.parse_and_create(**validated_data)


class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = ['id', 'number', 'content']


class SimilarSentencesSerializer(serializers.Serializer):
    source = SentenceSerializer(read_only=True)
    similar = SentenceSerializer(many=True, read_only=True)


class TextSerializer(serializers.ModelSerializer):
    sentences = SentenceSerializer(many=True, read_only=True)

    class Meta:
        model = Text
        fields = ['id', 'title', 'created_at', 'sentences']
