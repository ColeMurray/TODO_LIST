function AddTaskViewModel(){
    var self = this;
    self.title = ko.observable();
    self.description = ko.observable();

    self.addTask = function() {
        $('#add').modal('hide');
        tasksViewModel.add({
            title:self.title(),
            description:self.description()
        });
        self.title("");
        self.description("");
    }
}


