from django.contrib import admin

from .models import Quiz, Question, Answer, QuizTaker, CategoryTag

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuizTaker)
admin.site.register(CategoryTag)
