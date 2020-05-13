from rest_framework import serializers
from .models import Text, Sentence


class NewTextSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=False, max_length=200)
    content = serializers.CharField(required=True, allow_blank=False, trim_whitespace=True, max_length=100000, write_only=True)

    def create(self, validated_data):
        return Text.parse_and_create(**validated_data)


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['id', 'title', 'created_at']


class SentenceSerializer(serializers.ModelSerializer):
    text = TextSerializer(read_only=True, required=False)
    class Meta:
        model = Sentence
        fields = ['id', 'number', 'content', 'text']


class SimilarSentenceSerializer(serializers.Serializer):
    similarity = serializers.FloatField(read_only=True)
    sentence = SentenceSerializer(read_only=True)


class SimilarTextSerializer(serializers.Serializer):
    text = TextSerializer()
    similar_sentences = SimilarSentenceSerializer(many=True, read_only=True)


class TextDetailSerializer(serializers.ModelSerializer):
    sentences = SentenceSerializer(many=True, read_only=True)

    class Meta:
        model = Text
        fields = ['id', 'title', 'created_at', 'sentences']
