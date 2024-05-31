from django.db import models


class Quiz(models.Model):
  name = models.CharField(max_length=300)


class Question(models.Model):
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
  text = models.CharField(max_length=300)


class Answer(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  text = models.CharField(max_length=300)
  is_correct = models.BooleanField(default=False)

class QuizTaker(models.Model):

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)

    NO_CODING = 'NOCD'
    BEGINNER = 'BGNR'
    INTERMEDIATE = 'INTR'
    ADVANCED = 'ADVD'

    self_reported_ability_choices = [
        (NO_CODING, 'No Coding Experience'),
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced')
    ]

    programming_ability = models.CharField(max_length=4, choices=self_reported_ability_choices, default=BEGINNER)

    def __str__(self):
        return self.first_name + " " + self.last_name
    
# if we want to give questions tags
class CategoryTag(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    tags = models.ManyToManyField(Question)

    def __str__(self):
        return self.name

