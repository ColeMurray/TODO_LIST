var taskViewModel = new TasksViewModel();
var addTaskViewModel = new AddTaskViewModel();
ko.applyBindings(taskViewModel, $('#main')[0]);
ko.applyBindings(addTaskViewModel, $('#add')[0]);
