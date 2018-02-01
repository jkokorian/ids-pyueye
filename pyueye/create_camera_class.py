#!usr/bin/python3
import jinja2
import re

template = """
import .ueye

class Camera():
    def __init__(self):
        

    {% for function in functions %}
    def {{function.name}}(self, {{function.args}}):
        return ueye.is_{{function.name}}(self.hCam, {{function.args}})
    {% endfor %}
"""


function_parser = re.compile(r'def is_(?P<name>.*)\(hCam,\s*(?P<args>.*)\):')

with open('./methods_headers.txt') as f:
    functions = [match.groupdict() for line in f for match in function_parser.finditer(line)]



with open('camera.py','w') as f:
    f.write(jinja2.Template(template).render({'functions': functions}))

    


    