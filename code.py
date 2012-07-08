#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
toodledo2grwol : Display grwol notify tasks of Toodledo

"""
from datetime import datetime
from poodledo.apiclient import ApiClient
import gntp.notifier
import logging

# Task Filters
def _taskFilter(tasks):
    """
     Task Filter -- return filtered tasks
    """

    def _isUncompleted(task):
        """
         Task Uncompleted 
        """
        if hasattr(task, "completed") == False:
            logging.debug(': '.join(['not completed', task.title]))
            return True
        else:
            if task.completed == 0:
                logging.debug(': '.join(['not completed', task.title,
                    str(task.completed)]))
                return True
            else:
                logging.debug(': '.join(['completed', task.title,
                    str(task.completed)]))
                return False

    def _hasDuedate(task):
        """
         Task Has Duedate
        """
        if hasattr(task, "duedate") == True:
            if task.duedate != 0:
                logging.debug(': '.join(['has duedate', task.title]))
                return True
            else:
                logging.debug(': '.join(['has not duedate', task.title]))
                return False
        else:
            logging.debug(': '.join(['has duedate', task.title]))
            return False

    for task in [ task for task in tasks if (_isUncompleted(task) == True) and \
                                            (_hasDuedate(task) == True)]:
        yield task

# config logging
logging.basicConfig(level=logging.DEBUG)

# create Toodledo Client
api = ApiClient(app_id = "toodledo2growl", app_token="api4e7425e2854a8")
logging.info('created Toodledo Client')

# Toodledo Authentication
api.authenticate('morinatsu@gmail.com', 'uthena')
logging.info('Auth Toodledo')

# Get Task list from Toodledo
task_list = api.getTasks(fields="duedate")
logging.info(': '.join(['Got task list', str(len(task_list))]))

# Register to Growl
growl = gntp.notifier.GrowlNotifier(
    applicationName = "toodledo2growl",
    notifications = ["Task"],
    defaultNotifications = ["Task"],
)
growl.register()
logging.info('Register growl')

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
    logging.info(': '.join(['notify sended', hot_task.title]))
# end
logging.info('end')

