
"""Module defining Mutliple classes for scheduling tasks and activities."""

class Time:
    """
    A class representing a point in time that can be used with other classes in this module.
    a point in time is represented by hour and minute attributes.
    Supports addition with duration in minutes.
    """
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute
    
    def __add__(self, duration):
        minutes = self.minute + duration
        hours = self.hour + minutes // 60
        minutes = minutes % 60
        return Time(hours, minutes)
    def __str__(self):
        return f"{self.hour:02}:{self.minute:02}"
    
    @staticmethod
    def parse_time(time_str):
        """Parses a time string in the format 'hh-mm' and returns a Time object."""
        hour, minute = map(int, time_str.split('-'))
        return Time(hour, minute)

class Task:
    """
    A class representing a Task with the following properties :
    - task_id : an iderntifier (preferably unique) for each task, if None is given, an auto-generated int id will be assigned
    - name : name of the task
    - description : description of the task
    - start_time : an object representing the start time of the task
    - end_time : an object representing the end time of the task
    - priority : priority level of the task
    """
    def __init__(self, task_id, name, description, start_time, end_time, priority):
        self.id = Task.get_id(task_id)
        self.name = name
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.priority = priority

    auto_id = 0
    @staticmethod
    def get_id(id):
        if id is None:
            Task.auto_id += 1
            return Task.auto_id
        return id
    
    @staticmethod
    def default_format(task):
        """
        default formatting function, returns a string representation of the task in the following format :

        [id] name (start_time-end_time) Priority: priority :: description
        """
        return f"[{task.id}] {task.name} ({task.start_time}-{task.end_time}) Priority: {task.priority} :: {task.description}"

    def get_name(self): return self.name
    def set_name(self, name): self.name = name
    def get_description(self): return self.description
    def set_description(self, description): self.description = description
    def get_start_time(self): return self.start_time
    def set_start_time(self, start_time): self.start_time = start_time
    def get_end_time(self): return self.end_time
    def set_end_time(self, end_time): self.end_time = end_time
    def get_priority(self): return self.priority
    def set_priority(self, priority): self.priority = priority


class Activity:
    """
    A class representing an Activity with the following properties :
    - name : name of the activity
    - start_time : an object representing the start time of the activity
    - duration : duration of the activity in minutes
    """
    def __init__(self, name, start_time, duration):
        self.name = name
        self.start_time = start_time
        self.duration = duration
    
    @staticmethod
    def default_format(activity):
        start_time = activity.start_time
        return f"{activity.name} ({start_time}-{start_time + activity.duration})"


if __name__ == "__main__":
    from containers import Array

    schedule = Array([])

    print("Welcome to the schedule app")
    print("Enter 'l' to list all tasks")
    print("Enter 'a' to add a new task")
    print("Enter 'q' to quit")

    choice = input("Enter your choice: ")

    while choice != 'q':

        if choice == 'l':
            schedule.print(format=Activity.default_format)
        elif choice == 'a':
            name = input("Enter task name: ")
            description = input("Enter task description: ")
            start_time = Time.parse_time(input("Enter start time hh-mm: "))
            end_time = Time.parse_time(input("Enter end time hh-mm: "))
            priority = int(input("Enter task priority (1-10): "))

            task = Task(None, name, description, start_time, end_time, priority)
            schedule.append(task)

            print("Task added successfully!")
        else:
            print("Invalid choice!")

        choice = input("Enter your choice: ")

    print("Goodbye!")