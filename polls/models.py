from django.db import models

class Poll(models.Model):
    poll_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    end_date = models.DateTimeField()
    poll_description = models.CharField(max_length=200)

    def __str__(self):
        return self.poll_name


class Question(models.Model):
    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    question_type = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text


class Answer(models.Model):
    user_id = models.IntegerField(null=True)
    poll = models.ForeignKey(Poll, related_name='poll', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='question', on_delete=models.CASCADE)
    choice = models.CharField(max_length=200, null=True)
    choice_text = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.choice_text