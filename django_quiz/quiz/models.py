from django.db import models

class Quiz(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPES, default='MC')
    correct_answer = models.CharField(max_length=200)
    option1 = models.CharField(max_length=200, blank=True, null=True)
    option2 = models.CharField(max_length=200, blank=True, null=True)
    option3 = models.CharField(max_length=200, blank=True, null=True)
    option4 = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.question_text

class Answer(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  text = models.CharField(max_length=300)
  is_correct = models.BooleanField(default=False)

# to collect quiz taker data
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
# bare bones example
