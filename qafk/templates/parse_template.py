import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import xml.etree.ElementTree as ET
import argparse
import jinja2
import os

parser = argparse.ArgumentParser()
parser.add_argument("template_file_name")
args = parser.parse_args()



app = QApplication(sys.argv)
 
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
                    
                
            
        # if el.tag == 'widget' and parent !=None:
        #     parent.addWidget(elem)

        return elem
            
        
    def parse(self, extras = {}):
        tree = ET.parse(self.template_file)
        root = tree.getroot()
        if root.tag != "template":
            raise ViewNotFound
        return self._parse(root, extras = extras)
        
        


if args.template_file_name:
    main_dialog = QDialog()
    app.processEvents()
    template_file = args.template_file_name
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
    temp_jinja = env.get_template(template_file).render()
    jj_temp_file = template_file + ".jj"
    open(jj_temp_file, "w").write(temp_jinja)
    template_parser = TemplateParser(jj_temp_file)
    extras = {}
    view = template_parser.parse(extras)
    os.remove(jj_temp_file)
    if 'title' in extras:
        main_dialog.setWindowTitle(extras['title'])
    main_dialog.setLayout(view)
    main_dialog.show()
    
sys.exit(app.exec_())
