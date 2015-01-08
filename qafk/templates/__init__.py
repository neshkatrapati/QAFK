from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import xml.etree.ElementTree as ET
import argparse
import jinja2
import importlib
import os




def call_method(method, container, args):
    def _method(event):
        return  method(container, args)
    return _method



class ViewNotFound(Exception):
    pass
class LayoutTypeNotFound(Exception):
    pass
class WidgetTypeNotFound(Exception):
    pass



class TemplateMethods(object):
    @staticmethod
    def setText(element, xmlel):
        element.setText(QString(xmlel.text))

class TemplateParser(object):
    layouts = {
        'vbox' : QVBoxLayout,
        'hbox' : QHBoxLayout
    }
    widgets = {
            "label": QLabel,
            "button" : QPushButton,
            "text" : QLineEdit,
            "textbox" : QTextEdit,
            "combo" : QComboBox,
            "checkbox": QCheckBox,
            "slider": QSlider,
            "calendar":QCalendarWidget,
            "radio": QGroupBox,
            "listcheck": QListView}

    attributes = {
        'label': {
            'text' : TemplateMethods.setText
        },
        'button' : {
            'text' : TemplateMethods.setText
        }
    }
    def __init__(self, template_file):

        self.template_file = template_file

    def get_element(self, element_type, element_sub_type):
        if element_type == 'layout':
            if element_sub_type not in self.layouts:
                raise LayoutTypeNotFound
            return self.layouts[element_sub_type]
        elif element_type == 'widget':
            if element_sub_type not in self.widgets:
                raise WidgetTypeNotFound
            return self.widgets[element_sub_type]


    def _parse(self, el, parent=None, extras = {}):
        elem = None
        if el.tag == "layout" or el.tag == 'widget':
            elem = self.get_element(el.tag, el.attrib['type'])()


        for child in el:

            if child.tag == "layout" or child.tag == 'widget':
                comp = self._parse(child, parent=elem, extras=extras)
                if elem != None and comp !=None:
                    if child.tag == 'layout':
                        elem.addLayout(comp)
                    elif child.tag == 'widget':
                        stretch = 1
                        if 'stretch' in child.attrib:
                            stretch = int(child.attrib['stretch'])
                        elem.addWidget(comp, stretch)
                elif comp != None and child.tag == 'layout':
                    elem = comp

            elif child.tag == "title":
                extras['title'] = child.text

            elif elem != None and el.attrib['type'] in self.attributes:
                attr_list = self.attributes[el.attrib['type']]
                if child.tag in attr_list:
                    method = attr_list[child.tag]
                    method(elem, child)
                    elem.repaint()
                    elem.update()


            if elem !=None and el.attrib != None and 'onclick' in el.attrib:
                module_parts = el.attrib['onclick'].split('.')
                module_path = ".".join(module_parts[:-1])
                module = importlib.import_module(module_path)
                dview = module.__dict__[module_parts[-1]]
                elem.clicked.connect(call_method(dview, self.container, None))


        if elem !=None and el.attrib != None and 'name' in el.attrib:

            setattr(self.container, el.attrib['name'], elem)

        # if el.tag == 'widget' and parent !=None:
        #     parent.addWidget(elem)

        return elem


    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():

                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.close()
                else:
                    self.clearLayout(item.layout())

    def render(self, container, args):
        self.container = container
        env = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
        temp_jinja = env.get_template(self.template_file).render(**args)
        jj_temp_file = self.template_file + ".jj"
        open(jj_temp_file, "w").write(temp_jinja)
        tree = ET.parse(jj_temp_file)
        root = tree.getroot()
        if root.tag != "template":
            raise ViewNotFound
        extras = {}
        parsed_view = self._parse(root, extras = extras)

        # if container.parsed_view != None:
        #     self.clearLayout(container.parsed_view)
        #     self.container.parsed_view.deleteLater()

        if 'title' in extras:
            container.container.setWindowTitle(extras['title'])

        self.clearLayout(container.container.layout())
        QObjectCleanupHandler().add(container.container.layout())
        # print container.parsed_view, container.container.layout()
        # container.parsed_view = parsed_view
        container.container.setLayout(parsed_view)






