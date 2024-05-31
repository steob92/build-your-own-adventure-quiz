
from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Question

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    if request.method == 'POST':
        score = 0
        for question in questions:
            user_answer = request.POST.get(f'question_{question.id}')
            if user_answer and user_answer.lower() == question.correct_answer.lower():
                score += 1
        return render(request, 'quiz/quiz_result.html', {'quiz': quiz, 'score': score, 'total': len(questions)})
    return render(request, 'quiz/take_quiz.html', {'quiz': quiz, 'questions': questions})

def create_quiztaker(request):
    if request.method == 'POST':
        form = QuizTakerForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('success'):
    else:
        form = QuizTakerForm()
    
    return render(request, 'create_quiztaker.html', {'form': form})