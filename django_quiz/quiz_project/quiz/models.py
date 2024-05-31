from django.db import models

class Quiz(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

# bare bones example
