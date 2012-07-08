#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
toodledo2grwol : Display grwol notify tasks of Toodledo

"""
from datetime import datetime
from poodledo.apiclient import ApiClient
import gntp.notifier

# Task Filters
def _taskFilter(tasks):
    """
     Task Filter -- return filtered tasks
    """

    def _isUncompleted(task):
        """
         Task Uncomplered 
        """
        if hasattr(task, "completed") == False:
            return True
        else:
            if task.completed == "0":
                return True
            else:
                return False

    def _hasDuedate(task):
        """
         Task Has Duedate
        """
        if hasattr(task, "duedate") == True:
            if task.duedate != "0":
                return True
            else:
                return False
        else:
            return False

    for task in [ task for task in tasks if (_isUncompleted(task) == True) and \
                                            (_hasDuedate(task) == True)]:
        yield task

# create Toodledo Client
api = ApiClient(app_id = "toodledo2growl", app_token="api4e7425e2854a8")

# Toodledo Authentication
api.authenticate('morinatsu@gmail.com', 'uthena')

# Get Task list from Toodledo
task_list = api.getTasks(fields="duedate")

# Register to Growl
growl = gntp.notifier.GrowlNotifier(
    applicationName = "toodledo2growl",
    notifications = ["Task"],
    defaultNotifications = ["Task"],
)
growl.register()

# Send Notify to Growl
for hot_task in _taskFilter(task_list):
    duedate = datetime.fromtimestamp(float(hot_task.duedate))
    growl.notify(
        noteType = "Task",
        title = hot_task.title,
        description = duedate.strftime("DueDate: %Y/%m/%d"),
        icon = "file:///C:/Users/nmori/Documents/toodledo2growl/cafepress.png",
        sticky = False,
        priority = 1,
    )
# end

