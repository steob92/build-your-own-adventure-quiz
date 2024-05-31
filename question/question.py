import subprocess
import tempfile 
from importlib.util import spec_from_file_location, module_from_spec
import sys
import os

class Question():

    def __init__(self):

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

        self.__common_errors__ = """
    This is an message with some common errors that are expected
"""

    def test_answer(self, input):

        try:
            assert(input == self.solution)
            return (True, self.solution_string)
        
        except AssertionError as err_msg:
            return (False, self.error_string, err_msg)
        
        except ImportError as err_msg:
            print (self.__common_errors__)
            return (False, self.error_string, err_msg)

    def run_answer(self, input):
        # Step 1: Create a temporary Python file
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as temp:
            # Step 2: Write the Python code to the temporary file
            # temp.write("def temporary_function():\n")
            temp.write(input)  # Use 4 spaces for indentation

            temp_file_path = temp.name

        # Step 3: Import the function from the temporary file
        try:
            spec = spec_from_file_location("tmp_mod", temp_file_path)
            if spec and spec.loader:
                temporary_module = module_from_spec(spec)
                sys.modules["tmp_mod"] = temporary_module
                spec.loader.exec_module(temporary_module)

                # Call the function from the temporary module
                result = temporary_module.my_test(*self.test_args)

                # Test the answer
                stuff = self.test_answer(result)
                return stuff
            else:
                raise ImportError("Could not load temporary module")
        finally:
            # Clean up the temporary file
            os.remove(temp_file_path)
