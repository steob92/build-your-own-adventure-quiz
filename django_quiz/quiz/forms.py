from django import forms
from .models import QuizTaker

class QuizTakerForm(forms.ModelForm):
    
    class Meta:
        model = QuizTaker
        fields = ['first_name', 'last_name', 'programming_ability']
        widgets = {
            'programming_ability': forms.Select(choices=QuizTaker.self_reported_ability_choices)
        }
        