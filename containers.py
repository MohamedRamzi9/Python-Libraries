"""
- app to create schedules for items
- the schedule is a list of items
- the app should be able to :
    - append items
    - instert at a specific position
    - get number of items
    - remove items
    - get items by name (regex), id, index
    - modify items details 
    - reorder items by priority, start time, or end time
    - reorder items manually via a list of ids, indexes, or names
    - iterate over items
    - write the schedule to any output stream (allow the user to define the format of each item)
    - print the schedule to console

- some predefined items are :
    - Task : has the following properties :
        - a name
        - a description
        - a start time : object representing a point in time
        - an end time : same as start time
        - a priority
        - an id (either auto-generated or user-defined)
    - Activity : has the following properties :
        - a name
        - a start time : object representing a point in time
        - a duration : in minutes
"""

from io import StringIO


class Task:
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

    class Time:
        def __init__(self, hour, minute):
            self.hour = hour
            self.minute = minute
        
        def __add__(self, duration):
            minutes = self.minute + duration
            hours = self.hour + minutes // 60
            minutes = minutes % 60
            return Activity.Time(hours, minutes)
        def __str__(self):
            return f"{self.hour:02}:{self.minute:02}"
        
    def __init__(self, name, start_time, duration):
        self.name = name
        self.start_time = start_time
        self.duration = duration
    
    @staticmethod
    def default_format(activity):
        start_time = activity.start_time
        return f"{activity.name} ({start_time}-{start_time + activity.duration})"

class Schedule:

    class Wrapper:
        def __init__(self, item, index):
            self.item = item
            self.index = index

    def __init__(self, items):
        self.items = items

    def append(self, task):
        self.items.append(task)
    
    def insert(self, index, task):
        self.items.insert(index, task)

    def count(self):
        return len(self.items)
    
    def remove(self, task_wrapper): 
        self.items.pop(task_wrapper.index)

    def get_by_index(self, index):
        return Task.Wrapper(self.items[index], index)
    def get(self, filter):
        for index, task in enumerate(self.items):
            if filter(task):
                return Task.Wrapper(task, index) 
        return None

    def reorder(self, key, decending=True):
        self.items.sort(key=key, reverse=decending)

    def reorder_exact(self, order, key):
        for index in range(len(order)):
            for i, task in enumerate(self.items):
                if key(task) == order[index]:
                    self.items[index], self.items[i] = self.items[i], self.items[index]
                    break

    def write(self, output, format):
        for item in self.items:
            output.write(format(item) + "\n")

    def print(self, format):
        output = StringIO()
        self.write(output, format)
        print(output.getvalue())

    # ========== Helpers ==========

    def __iter__(self):
        for index, item in enumerate(self.items):
            yield self.wrapper(item, index)
    def wrapper(self, item, index):
        return Schedule.Wrapper(item, index)


if __name__ == "__main__":
    schedule = Schedule([])

    schedule.append(Activity("Activity 1", Activity.Time(9, 0), 60))
    schedule.append(Activity("Activity 2", Activity.Time(10, 30), 90))
    schedule.append(Activity("Activity 3", Activity.Time(13, 0), 120))

    schedule.print(Activity.default_format)