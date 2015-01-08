from pony.orm import *
from settings import *

class DB(object):
    def __init__(self):
        self.db = Database()
    def connect(self, params):
        if params['db_type'] == 'sqlite':
            self.db.bind('sqlite', params['database'], create_db=True)
        elif params['db_type'] == 'postgres':
            self.db.bind('postgres', host=params["host"],
                    user=params["user"],
                    password=params["password"],
                    database=params['database'])
        elif params['db_type'] == 'mysql':
            self.db.bind('postgres', host=params["host"],
                    user=params["user"],
                    passwd=params["password"],
                    db=params['database'])



db = DB()
db.connect(DATABASE)
