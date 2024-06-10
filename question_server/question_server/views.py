import json
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from .question.question import question_from_dict
from .models import Question



# @csrf_exempt  # Use this decorator to exempt the view from CSRF verification (only for development/testing purposes)
# def my_view(request):
#     if request.method == 'POST':
#         try:
#             # Parse the JSON data from the request body
#             data = json.loads(request.body)
#             message = data.get('message', 'No message provided')
#             response = {
#                 'received_message': message,
#                 'status': 'success'
#             }
#             return JsonResponse(response, status=200)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)
#     else:
#         return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

@csrf_exempt
def view_all_questions(request):
    """
    A view to retrieve all available questions by name.
    """
    questions = Question.objects.all()
    question_names = [question.name for question in questions]
    return JsonResponse({'questions': question_names})

# Create your views here.
@csrf_exempt
def question_detail(request, question_name):
    try:
        question = Question.objects.get(name=question_name)
        data = {
            'name': question.name,
            'about': question.about,
            'info': question.info,
            'help': question.help,
            'solution': question.solution,
            'solution_string': question.solution_string,
            'error_string': question.error_string,
            'test_args': question.test_args,
            'TIMEOUT': question.TIMEOUT,
            'common_errors': question.common_errors,
        }
        if request.method == 'GET':

            return JsonResponse(data)
        elif request.method == 'POST':

            print ("Here is the request body: ", request.body)
            test_question = question_from_dict(data)

            q_data = json.loads(request.body)
            func_string = q_data.get('user_input', 'No message provided')
            print (func_string)
            res = test_question.run_answer(func_string)
            res = {"status" : res[0], "message" : res[1], "exception" : res[2] }
            print (res)
            return JsonResponse(res, status=200)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")