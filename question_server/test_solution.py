from question.function_1 import FunctionQuestion


my_function = """
def my_test(a, b):
    import time
    time.sleep(10)
    return a + b
"""

my_question = FunctionQuestion()

stuff = my_question.run_answer(my_function)
print (stuff)