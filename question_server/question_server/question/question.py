import multiprocessing
import multiprocessing.spawn
import tempfile 
from importlib.util import spec_from_file_location, module_from_spec
import sys
import os
import time
import yaml


def question_from_dict(question_dict):
    new_question = Question()
    new_question.name = question_dict['name']
    new_question.about = question_dict['about']
    new_question.info = question_dict['info']
    new_question.help = question_dict['help']
    new_question.solution = question_dict['solution']
    new_question.solution_string = question_dict['solution_string']
    new_question.error_string = question_dict['error_string']
    new_question.test_args = question_dict['test_args']
    new_question.imports = question_dict['imports']

    if 'TIMEOUT' not in question_dict:
        new_question.TIMEOUT = 5
    else:
        new_question.TIMEOUT = question_dict['TIMEOUT']
    if "common_errors" not in question_dict:
        new_question.common_errors = ""
    else:
        new_question.common_errors = question_dict['common_errors']
    return new_question

def question_from_yaml(yaml_file):
    new_question = Question()
    
    with open(yaml_file, 'r') as stream:
        try:
            question_dict = yaml.safe_load(stream)
            new_question.name = question_dict['name']
            new_question.about = question_dict['about']
            new_question.info = question_dict['info']
            new_question.help = question_dict['help']
            new_question.solution = question_dict['solution']
            new_question.solution_string = question_dict['solution_string']
            new_question.error_string = question_dict['error_string']
            new_question.test_args = question_dict['test_args']
            new_question.imports = question_dict['imports']

            if 'TIMEOUT' not in question_dict:
                new_question.TIMEOUT = 5
            else:
                new_question.TIMEOUT = question_dict['TIMEOUT']
            if "common_errors" not in question_dict:
                new_question.common_errors = ""
            else:
                new_question.common_errors = question_dict['common_errors']
        except yaml.YAMLError as exc:
            print(exc)
    return new_question

def load_questions_from_dir(directory):
    questions = {}
    for filename in os.listdir(directory):
        if filename.endswith(".yaml"):
            qname = filename.split("/")[-1].split(".")[0]
            questions[qname] = question_from_yaml(os.path.join(directory, filename))
    return questions

class Question():

    def __init__(self):
        self.name = "tmp_question"
        self.TIMEOUT = 5
        self.about = ""
        self.info = """
    This is an info string    
"""
        self.help = """
    This is a useful help sting
    """
        
        # Set the answer to the problem
        self.solution = True
        # Solution string to provide some information on the learning objection
        self.solution_string = """
    This is a description of what happens 
"""

        self.error_string = """
    This is a error string that will provide links to useful resources
"""
        self.test_args = ()

        self.common_errors = """
    This is an message with some common errors that are expected
"""

    def test_answer(self, input):

        test_solution = type(input)(self.solution)
        try:
            assert(input == test_solution)
            return (True, self.solution_string, "The answer is correct")
        
        except AssertionError as err_msg:
            print (self.error_string, err_msg)
            return (False, self.error_string, "The answer is not correct")
        
        except ImportError as err_msg:
            print (self.common_errors)
            return (False, self.error_string, "An error occurred: " + str(err_msg))

    def run_answer(self, input):
        # Step 1: Create a temporary Python file
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as temp:
            # print (self.imports)
            for imp in (
                self.imports.replace("[", "").replace("]", "")
                    .replace("\'","").replace("\"","").split(", ")
            ):
                
                temp.write(imp + "\n")
            # Step 2: Write the Python code to the temporary file
            for line in input.split("\n"):
                # prevent the user from importing modules
                if "import" in line:
                    continue
                temp.write(line + "\n")
            # temp.write(input)
            
            temp_file_path = temp.name
        # with open(temp_file_path, "r") as f:
        #     print (f.read())

        # Step 3: Import the function from the temporary file
        try:
            spec = spec_from_file_location("tmp_mod", temp_file_path)
            if spec and spec.loader:
                temporary_module = module_from_spec(spec)
                sys.modules["tmp_mod"] = temporary_module
                spec.loader.exec_module(temporary_module)

                # Call the function from the temporary module
                with multiprocessing.Pool(1) as pool:
                    # p = pool.map_async(temporary_module.my_test, self.test_args)
                    # Create a Queue to get the result from the child process
                    queue = multiprocessing.Queue()

                    # Define a wrapper function to call the test function and put the result in the queue
                    def wrapper(queue, *args):
                        result = temporary_module.my_test(*args)
                        queue.put(result)

                    # Start the process
                    p = multiprocessing.Process(target=wrapper, args=(queue, *self.test_args))
                    p.start()
                    t = 0
                    exit_success = False
                    while t < self.TIMEOUT:
                        if p.is_alive():
                            time.sleep(0.1)
                            t += 0.1
                        else:
                            exit_success = True
                            break

                    if exit_success:
                        # Get the result from the queue
                        result = queue.get()
                        print (result, type(result))    
                        os.remove(temp_file_path)
                        return self.test_answer(result)
                    else:
                        # Timeout handling
                        p.terminate()
                        os.remove(temp_file_path)
                        return (False, self.error_string, "Program took too long!")
                        # raise TimeoutError("Program took too long!")

            else:
                os.remove(temp_file_path)
                return (False, self.error_string, "Could not load temporary module")
                # raise ImportError("Could not load temporary module")

        except Exception as e:
            os.remove(temp_file_path)
            return (False, self.error_string, "An error occurred: " + str(e))

