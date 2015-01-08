from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ContainerManager (object):
    def __init__(self):
        self.containers = {}
        
    def new_container(self,name):
        container = Container(name, self)
        self.containers[name] = container
        return container
        

        

class Container (object) :

    def __init__(self, name, manager):
        self.container = QWidget()
        self.manager = manager
        self.parsed_view = None

    def load_template_view(self, template_view):
        self.container.setLayout(template_view)
