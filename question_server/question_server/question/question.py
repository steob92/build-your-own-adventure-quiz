import multiprocessing
import multiprocessing.spawn
import tempfile 
from importlib.util import spec_from_file_location, module_from_spec
import sys
import os
import time

class Question():

    def __init__(self):

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

        self.__common_errors__ = """
    This is an message with some common errors that are expected
"""

    def test_answer(self, input):

        try:
            assert(input == self.solution)
            return (True, self.solution_string, "")
        
        except AssertionError as err_msg:
            return (False, self.error_string, err_msg)
        
        except ImportError as err_msg:
            print (self.__common_errors__)
            return (False, self.error_string, err_msg)

    def run_answer(self, input):
        # Step 1: Create a temporary Python file
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as temp:
            # Step 2: Write the Python code to the temporary file
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
                        return self.test_answer(result)
                    else:
                        # Timeout handling
                        p.terminate()
                        raise TimeoutError("Program took too long!")


                # Test the answer
                # should be ran as a subprocess
                # stuff = subprocess.run(self.test_answer(result))
            else:
                raise ImportError("Could not load temporary module")
        finally:
            # Clean up the temporary file
            os.remove(temp_file_path)
