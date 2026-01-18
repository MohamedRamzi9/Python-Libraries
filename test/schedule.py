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