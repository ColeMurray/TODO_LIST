# TODO_LIST

Todo list is a restful service implemented in Flask.
Todo list allows for users to register accounts and
create tasks to be completed.

##Documentation
| Request | URL | Functionality |
|:---------|:------------------:|----------:|
| POST     | http://[hostname]/todo/api/v2/user/    | Register users      
| POST     | http://[hostname]/todo/api/v2/tasks   | Create new task     
| GET      | http://[hostname]/todo/api/v2/tasks   | Return user's tasks 
| GET      | http://[hostname]/todo/api/v2/tasks/id | Get task by id
| DELETE   | http://[hostname]/todo/api/v2/tasks/id | Delete task

