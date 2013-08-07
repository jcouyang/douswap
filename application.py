from flask import Flask, jsonify, g, request, _request_ctx_stack
from flask.ext.restful import Api, Resource
from flask.ext.login import login_required, LoginManager,current_user,login_user
import pprint
from douban_client import DoubanClient
from config import *
from modle import *
from bson.json_util import dumps
app = Flask(__name__)
api = Api(app)
app.secret_key = 'g4KTAbXmcEj7AO'
class TokenLoginManager(LoginManager):
    def reload_user(self):
        if request.headers.has_key('Authorization'):
            ctx = _request_ctx_stack.top
            ctx.user = self.token_callback(request.headers['Authorization'])
            return
        super(TokenLoginManager,self).reload_user()

login_manager = TokenLoginManager()

login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return connection.User.find_one({'id':id})
@login_manager.token_loader
def token_loader(token):
    return connection.User.find_one({'password':token})

@app.before_request
def before_request():
    g.user = current_user

class UserAPI(Resource):
    @login_required
    def get(self):
        return dumps(current_user)


class Login(Resource):
    def get(self,code):
        douban = DoubanClient(API_KEY, SECRET, 'http://book.douban.com',SCOPE)
        douban.auth_with_code(code)
        token = douban.access_token.token
        print token
        duser = douban.user.me
        print duser
        user = connection.User()
        user['id']=int(duser['uid'])
        user['password'] = token
        user.save()
        return token

class BookAPI(Resource):
    def get(self, id):
        pass

api.add_resource(UserAPI, '/user')
api.add_resource(Login, '/login/<string:code>')

@app.route('/')
def hello_world():
    return AUTH_URI

if __name__ == '__main__':
    app.run(debug=True)
