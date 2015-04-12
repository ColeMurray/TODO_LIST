from app import db

class User (db.Model):
    __tablename__ = 'user'
    id = db.Column (db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(10))
    tasks = db.relationship('Task', backref='author', lazy = 'dynamic')

    def is_Authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        try:
            return unicode(self.id) #python2
        except NameError:
            return str(self.id) #python3
    def __init__ (self,username,password):
        self.username = username
        self.password = password
    def __repr__(self):
        return '<User %r>' % (self.username)

class Task (db.Model):
    __tablename__ = 'tasks'
    id = db.Column (db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True, unique=False)
    description = db.Column (db.String(128), index=True, unique = False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __init__ (self,title,description,author):
        self.title = title
        self.description = description
        self.author = author

    def __repr__(self):
        return '<Task %r %r %r>' % (self.title,self.author,self.body)

    
