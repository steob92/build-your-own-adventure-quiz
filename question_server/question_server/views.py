import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .question.function_1 import FunctionQuestion




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


# Create your views here.
@csrf_exempt
def question_function_1(request):

    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            func_string = data.get('func', 'No message provided')
            print (func_string)
            myfunc = FunctionQuestion()
            res = myfunc.run_answer(func_string)
            res = {"status" : res[0], "message" : res[1], "exception" : res[2] }
            print (res)
            return JsonResponse(res, status=200)
        except Exception as e:
            print ("error...")
            print (e)

    return JsonResponse(data)