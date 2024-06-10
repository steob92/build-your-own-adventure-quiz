from django.db import models

class Question(models.Model):
    name = models.TextField()
    about = models.TextField()
    info = models.TextField()
    help = models.TextField()
    solution = models.TextField()
    solution_string = models.TextField()
    error_string = models.TextField()
    test_args = models.JSONField()
    TIMEOUT = models.IntegerField()
    common_errors = models.JSONField()

    def __str__(self):
        return self.about

    class Meta:
        app_label = 'question_server'