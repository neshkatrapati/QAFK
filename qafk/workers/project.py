import os
import sys
from qafk.console.text_styles import Color
class ProjectWorker(object):
    DEFAULT_SETTINGS = """
       DATABASE = {'type' : 'sqlite',
                   'host' : '',
                   'username' : '',
                   'password' : '',
                   'database' : 'test.db'
                  }
    """.strip()

    DEFAULT_RUN ="""
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qafk.containers import ContainerManager 
from {project_name}.views import *

app = QApplication(sys.argv)
container_manager = ContainerManager()
container = container_manager.new_container('main')
home(container)
container.container.show()
sys.exit(app.exec_())

"""
    
    DEFAULT_VIEWS ="""
from qafk.views import view
from qafk.templates import TemplateParser
@view('{project_name}', 'home')
def home(container, args=None):
    print "Home Sweet Home"
    return TemplateParser('{project_name}/templates/main.template').render(container, {{'message' : 'Hello !, Welcome to QAFK' }})
"""


    DEFAULT_TEMPLATES = """<template name='main'>
<title> Home </title>
<layout type='vbox' name='mainLayout'>
  <widget type='label' name='mainLabel'>
    <text> {{{{ message }}}} !! </text>
  </widget>
</layout>
</template>
"""
    @staticmethod
    def create_project(args):
        sys.stdout.write(
            Color.bold(Color.underline("Creating Project : {project_name}\n"
                                       .format(project_name=args.project_name))))

        sys.stdout.write(Color.underline("Creating Directory Structure\n"))

        os.mkdir(args.project_name)
        open(args.project_name + '/__init__.py', 'w').write("")

        os.mkdir(os.path.join(args.project_name,args.project_name))

        open(os.path.join(args.project_name,args.project_name) + '/__init__.py', 'w').write("")

        sys.stdout.write("  Creating Settings File\n")
       
        open(os.path.join(args.project_name,args.project_name) + '/settings.py', 'w').write(ProjectWorker.DEFAULT_SETTINGS)

        sys.stdout.write("  Creating {project_name}/views.py\n".format(project_name=args.project_name))
       
        open(os.path.join(args.project_name,args.project_name) + '/views.py', 'w').write(ProjectWorker.DEFAULT_VIEWS.format(project_name = args.project_name))

        sys.stdout.write("  Creating {project_name}/templates\n".format(project_name=args.project_name))

        os.mkdir(os.path.join(args.project_name,args.project_name) + '/templates')
        open(os.path.join(args.project_name,args.project_name) + '/templates/main.template', 'w').write(ProjectWorker.DEFAULT_TEMPLATES.format(project_name = args.project_name))

        sys.stdout.write("  Creating Launch File\n")
       
        open(args.project_name + '/run.py', 'w').write(ProjectWorker.DEFAULT_RUN.format(project_name = args.project_name))
        
