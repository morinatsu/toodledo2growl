#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
toodledo2grwol : Display grwol notify tasks of Toodledo

"""
import os.path
from datetime import datetime
import logging
import ConfigParser
import gntp.notifier
from tasks import HotList


# parse config
current_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(current_dir, 'toodledo2growl.cnf')
config = ConfigParser.SafeConfigParser()
config.read([config_file])


# Register to Growl
growl = gntp.notifier.GrowlNotifier(
    applicationName="toodledo2growl",
    notifications=["Task"],
    defaultNotifications=["Task"],
)
growl.register()
logging.info('Register growl')

# Send Notify to Growl
notify_icon = os.path.join(current_dir, config.get('icon', 'notify'))
hotlist = HotList()
for hot_task in hotlist.retrieve():
    if not hasattr(hot_task, "duedate"):
        duedate = ""
    elif hot_task.duedate == 0:
        duedate = ""
    else:
        duedate = datetime.fromtimestamp(float(hot_task.duedate)) \
            .strftime("DueDate: %Y/%m/%d")
    growl.notify(
        noteType="Task",
        title=hot_task.title,
        description=duedate,
        icon=open(notify_icon, 'rb').read(),
        sticky=False,
        priority=1,
    )
    logging.info(': '.join(['notify sended', hot_task.title]))
# end
logging.info('end')
