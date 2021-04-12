from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

users = { 
   'users_list' :
   [
      { 
         'id' : 'xyz789',
         'name' : 'Charlie',
         'job': 'Janitor',
      },
      {
         'id' : 'abc123', 
         'name': 'Mac',
         'job': 'Bouncer',
      },
      {
         'id' : 'ppp222', 
         'name': 'Mac',
         'job': 'Professor',
      }, 
      {
         'id' : 'yat999', 
         'name': 'Dee',
         'job': 'Aspring actress',
      },
      {
         'id' : 'zap555', 
         'name': 'Dennis',
         'job': 'Bartender',
      }
   ]
}

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def get_users():
   if request.method == 'GET':
      search_username = request.args.get('name')
      search_job = request.args.get('job')
      if search_username:
         subdict = {'users_list' : []}
         if search_job:
            for user in users['users_list']:
               if user['name'] == search_username and user['job'] == search_job:
                  subdict['users_list'].append(user)
         else:
            for user in users['users_list']:
               if user['name'] == search_username:
                  subdict['users_list'].append(user)
         return subdict
      return users
   elif request.method == 'POST':
      userToAdd = request.get_json()
      userToAdd["id"] = random_id()
      users['users_list'].append(userToAdd)
      resp = jsonify(success=True, data=userToAdd)
      resp.status_code = 201 #optionally, you can always set a response code. 
      # 200 is the default code for a normal response
      return resp
   elif request.method == 'DELETE':
      del_id = request.args.get('id')
      if del_id:
         users['users_list'] = [user for user in users['users_list']\
                                  if user['id'] != del_id]
      return users      
         

@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
   if request.method == "GET":
      if id:
         for user in users['users_list']:
           if user['id'] == id:
              return user
         return ({})
      return users
   
   if request.method == "DELETE":      
      new_userlist = [user for user in users['users_list']\
                                  if user['id'] != id]
      if len(new_userlist) != len(users['users_list']):
         resp = jsonify(success=True)
         resp.status_code = 204
         users['users_list'] = new_userlist 
         return resp
      resp = jsonify(success=False)
      resp.status_code = 404  
      return resp      



def random_id():
   return uuid.uuid4()