# question_server/management/commands/load_questions.py

import os
import yaml
from django.core.management.base import BaseCommand
from question_server.models import Question
import re

loader = yaml.SafeLoader
loader.add_implicit_resolver(
    u'tag:yaml.org,2002:float',
    re.compile(u'''^(?:
     [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
    |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
    |\\.[0-9_]+(?:[eE][-+][0-9]+)?
    |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
    |[-+]?\\.(?:inf|Inf|INF)
    |\\.(?:nan|NaN|NAN))$''', re.X),
    list(u'-+0123456789.'))

class Command(BaseCommand):
    help = 'Load questions from YAML files in the specified directory'

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str, help='Directory containing the YAML files')

    def handle(self, *args, **kwargs):
        directory = kwargs['directory']
        load_questions_from_dir(directory)
        self.stdout.write(self.style.SUCCESS('Successfully loaded questions from directory'))

def question_from_yaml(yaml_file):
    new_question = Question()
    with open(yaml_file, 'r') as stream:
        try:
            question_dict = yaml.load(stream, Loader=loader)
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

            if 'common_errors' not in question_dict:
                new_question.common_errors = ""
            else:
                new_question.common_errors = question_dict['common_errors']
            new_question.save()
        except yaml.YAMLError as exc:
            print(exc)
    return new_question

def load_questions_from_dir(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".yaml"):
            question_from_yaml(os.path.join(directory, filename))
