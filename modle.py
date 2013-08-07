from flask.ext.login import UserMixin
from mongokit import Connection, Document
from config import *

connection = Connection(MONGO_URI)

@connection.register
class User(Document, UserMixin):
    __collection__ = 'user'
    __database__ = 'douswap'
    structure = {
        'name':unicode,
        'id':int,
        'password':basestring,
        'rate':int,
        'loc_id':basestring
    }
    use_dot_notation = True
    def get_id(self):
        print self.id
        return self.id
    def get_auth_token(self):
        return self.password

    def is_authenticated(self):
        return True
