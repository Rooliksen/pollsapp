from rest_framework import serializers
from .models import Poll, Question, Choice, Answer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

class CurrentUserDefault(object):
    def set_context(self, serializer_field):
        self.user_id = serializer_field.context['request'].user.id

    def __call__(self):
        return self.user_id


""" class AnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(default=CurrentUserDefault())
    poll = serializers.SlugRelatedField(queryset=Poll.objects.all(), slug_field='id')
    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='id')
    choice = serializers.SlugRelatedField(queryset=Choice.objects.all(), slug_field='id', allow_null=True)
    choice_text = serializers.CharField(max_length=200, allow_null=True, required=False)

    class Meta:
        model = Answer
        fields = '__all__'

    def create(self, validated_data):
        return Answer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance """

class ChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='id')
    choice_text = serializers.CharField(max_length=200)

    def validate(self, attrs):
        try:
            obj = Choice.objects.get(question=attrs['question'].id, choice_text=attrs['choice_text'])
        except Choice.DoesNotExist:
            return attrs
        else:
            raise serializers.ValidationError('Choice already exists')

    class Meta:
        model = Choice
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(default=CurrentUserDefault())
    poll = serializers.SlugRelatedField(queryset=Poll.objects.all(), slug_field='id')
    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='id')
    choice_text = serializers.CharField(max_length=200, allow_null=True, required=False)
    choice = serializers.PrimaryKeyRelatedField(queryset=Choice.objects.all(), many=True)

    class Meta:
        model = Answer
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    poll = serializers.SlugRelatedField(queryset=Poll.objects.all(), slug_field='id')
    question_text = serializers.CharField(max_length=200)
    question_type = serializers.CharField(max_length=200)
    choices = ChoiceSerializer(many=True, read_only=True)

    def validate(self, attrs):
        question_type = attrs['question_type']
        if question_type == 'one' or question_type == 'multiple' or question_type=='text':
            return attrs
        raise serializers.ValidationError('Question type can be only one, multiple, text')

    class Meta:
        model = Question
        fields = '__all__'

class PollSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    poll_name = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    poll_description = serializers.CharField(max_length=200)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = '__all__'