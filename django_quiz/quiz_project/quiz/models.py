from django.db import models

class Quiz(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Question(models.Model):

    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

class Answer(models.Model):

    id = models.AutoField(primary_key=True)
    question = models.ManyToManyField(Question)
    answer_text = models.CharField(max_length=3000)
    is_correct = models.BooleanField()

    def __str__(self):
        return self.answer_text


# to collect quiz taker data
class QuizTaker(models.Model):

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)

    self_reported_ability_choices = {
        "NOCD" : "No Coding Experience",
        "BGNR" : "Beginner",
        "INTR" : "Intermediate",
        "ADVD" : "Advanced"
    }

    programming_ability = models.CharField(max_length=4, choices=self_reported_ability_choices,
                                           default="BGNR")

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
