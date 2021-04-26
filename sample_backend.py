from flask import Flask, request, jsonify
from flask_cors import CORS
from model_mongo import Model, User
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

@app.route('/users', methods=['GET', 'POST'])
def get_users():
   if request.method == 'GET':
      search_username = request.args.get('name')
      search_job = request.args.get('job')
      if search_username and search_job:
         users=User().find_by_name_and_job(search_username, search_job)
      elif search_username:  # updated for db_access
         users = User().find_by_name(search_username)
      elif search_job:
         users = User().find_by_job(search_username)
      else:  # updated for db_access
         users = User().find_all()
      return {"users_list": users}
   elif request.method == 'POST':
      userToAdd = request.get_json()
      # userToAdd['id'] = gen_random_id() # check for duplicate before appending.. todo
      # users['users_list'].append(userToAdd)
      # updated for db_access
      # make DB request to add user
      newUser = User(userToAdd)
      newUser.save()
      resp = jsonify(newUser), 201
      return resp
   # elif request.method == 'DELETE':
   #    del_id = request.args.get('id')
   #    if del_id:
   #       users['users_list'] = [user for user in users['users_list']\
   #                                if user['id'] != del_id]
   #    return users      
         

@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
   if request.method == "GET":
      user = User({"_id" : id})
      if user.reload():
         return user
      else:
         return jsonify({"error" : "User not fouond"}), 404
   
   elif request.method == "DELETE":      
      aser = User({"_id": id})
      resp = user.remove()
      if (resp['n'] == 1):
          return {}, 204
      else:
          return 

#@app.route('/users?name=<name>&job=<job>', methods=['GET'])
# def find_users_by_name_job(name, job):
#     subdict = {'users_list': []}
#     for user in users['users_list']:
#         if user['name'] == name and user['job'] == job:
#             subdict['users_list'].append(user)
#     return subdict

# def find_users_by_job(job):
#     subdict = {'users_list': []}
#     for user in users['users_list']:
#         if user['job'] == job:
#             subdict['users_list'].append(user)
#     return subdict

def random_id():
   return uuid.uuid4()