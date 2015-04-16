from app import app,db
from flask import Blueprint, g, render_template, jsonify, url_for, make_response
from flask.ext.restful import Api,Resource, reqparse, fields, marshal, abort
from app.mod_todo.models import User,Task
from flask.ext.httpauth import HTTPBasicAuth

api = Api(app)
auth = HTTPBasicAuth()
userfields = {
    'username' : fields.String,
    'password' : fields.String
}
taskfields = {
    'title' : fields.String,
    'description' : fields.String,
    'done' : fields.Boolean,
    'uri' : fields.Url('task')
}

@auth.error_handler
def unauthorized():
    return make_response( jsonify({ 'error' : 'unauthorized access'}),403)
@app.errorhandler(400)
def not_found(error):
    return make_response( jsonify({'error' : 'Bad request'}),400)
@app.errorhandler(404)
def not_found(error):
    return make_response( jsonify({'error' : 'Not Found'}),404)


@app.route('/')
def index():
    return render_template('todo/index.html')

class UserApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user', type=str, required=True,
                                    help = 'No Username provided',
                                    location = 'json')
        self.reqparse.add_argument('password', type=str, required=True,
                                    help = 'No password',
                                    location = 'json')
        super(UserApi,self).__init__()
    @auth.login_required
    def get(self):
        return { 'data' : 'Hello %s' % g.user.username }
        
    def post(self):
        args = self.reqparse.parse_args()
        print "POST"
        for arg in args:
            print arg
        username = args['user']
        password = args['password']
        if User.query.filter_by(username = username).first() is not None:
            abort(403) #existing user

        user = User(username,password)
        db.session.add(user)
        db.session.commit()
        
        return { 'result' : True }, 201

class TaskListApi(Resource):
    def __init__ (self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                    help = 'No Task Provided',
                                    location='json')
        self.reqparse.add_argument('description', type=str, default="",
                                    location='json')
        self.reqparse.add_argument('done', type=bool, default=False,
                                    location='json')
        super(TaskListApi,self).__init__()
    @auth.login_required
    def get(self):
        tasks = g.user.tasks.all()
        return {'tasks' : marshal(tasks,taskfields)}

       
    @auth.login_required
    def post(self):
        #Add post to DB
        #return post in JSON with 201
        args = self.reqparse.parse_args()
        username = g.user.username
        title = args['title']
        description = args['description']
        done = args['done']

        task = Task(title,description,done, g.user)
        db.session.add(task)
        db.session.commit()
        taskInDB = Task.query.get(task.id)
        return { 'task' : marshal(task,taskfields) },201

class TaskApi(Resource):
    def __init__ (self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('done', type=bool, location='json')
        super(TaskApi,self).__init__()
    @auth.login_required
    def get(self,id):
        args = self.reqparse.parse_args()
        task = Task.query.get(id)
        if task is None or task.author is not g.user:
            abort (404)
        
        return { 'result' : marshal(task,taskfields)}
    @auth.login_required
    def put(self,id):
        task = Task.query.get(id)
        args = self.reqparse.parse_args()
        title = args['title']
        description = args['description']
        done = args['done']

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if done is not None:
            task.done = done



            
        

        db.session.commit()
        task = Task.query.get(id)
        return { 'task' : marshal(task,taskfields)}
        #update task matching id in DB
    @auth.login_required
    def delete(self,id):
        #remove entry from DB
        task = Task.query.get(id)
        if task is None:
            abort(404)
        db.session.delete(task)
        db.session.commit()
        return { 'result' : 'true' }

@auth.verify_password
def verify_password(username,password):
    user = User.query.filter_by(username=username).first()
    if not user or not (user.password == password):
        return False
    g.user = user
    return True

api.add_resource(TaskListApi, '/todo/api/v2/tasks', endpoint = 'tasks')
api.add_resource(TaskApi, '/todo/api/v2/tasks/<int:id>', endpoint = 'task')
api.add_resource(UserApi, '/todo/api/v2/users', endpoint = 'user')



