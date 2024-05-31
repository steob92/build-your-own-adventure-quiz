from .question import Question


class FunctionQuestion(Question):

    def __init__(self):
        super().__init__()
        self.about = """In this section we'll test the input to a function"""
        self.info = """
            Write a function to add two numbers together 
        """
        self.help = """
            We're expection a function that takes in two arguements and returns one
        """
                
        # Set the answer to the problem
        self.solution = 5.2
        self.test_args = (2.1, 3.1)
        # Solution string to provide some information on the learning objection
        self.solution_string = """
            Congradulations
        """

        self.error_string = f"""
            Sorry this isn't the correct answer... \n\tExpected answer: {self.solution}
        """
