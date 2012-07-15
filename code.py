#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
toodledo2grwol : Display grwol notify tasks of Toodledo

"""
from datetime import datetime, timedelta
import logging
import argparse
import ConfigParser
from poodledo.apiclient import ApiClient
import gntp.notifier


# Hotlist Filter
def _HotlistFilter(account_info, tasks):
    """
     Hotlist Filter -- return tasks in Hotlist
    """

    def _isHot(task):
        """
        If a task in Hostlist returns True
        """

        # priority
        if not hasattr(account_info, "hotlistpriority"):
            logging.debug('hotlistpriority is not setted.')
        else:
            if task.priority < account_info.hotlistpriority:
                logging.debug(': '.join(['less priority', task.title,
                    str(task.priority)]))
                return False

        # duedate
        if not hasattr(account_info, "hotlistduedate"):
            logging.debug('hotlistduedate is not setted.')
        else:
            today = datetime.today()
            from_date = datetime.fromtimestamp(float(task.duedate)) - \
                timedelta(account_info.hotlistduedate)
            if today < from_date:
                logging.debug(': '.join(['duedate is far', task.title,
                    str(task.duedate)]))
                return False

        # star
        if not hasattr(account_info, "hotliststar"):
            logging.debug('hotliststar is not setted.')
        else:
            if account_info.hotliststar == '1':
                if task.star != '1':
                    logging.debug(': '.join(['not starred', tasl.title,
                        task.star, account_info.hotliststar]))
                    return False

        # status
        if not hasattr(account_info, "hotliststatus"):
            logging.debug('hotliststatus is not setted.')
        else:
            if account_info.hotliststatus == '1':
                if task.status != '1':
                    logging.debug(': '.join(['is not Next Action', task.title,
                        task.status, account_info.hotliststatus]))
                    return False

        logging.debug(' '.join([task.title, 'is in Hotlist.']))
        return True

    def _isUncompleted(task):
        """
         Task Uncompleted
        """
        if not hasattr(task, "completed"):
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

    for task in [task for task in tasks if (_isHot(task) and _isUncompleted(task))]:
        yield task

#parse arguments
loglevel = 'WARNING'
parser = argparse.ArgumentParser(
    description='Notify toodledo tasks with Growl for windows.')
parser.add_argument('--log', dest='loglevel', default='WARNING',
    help='level of logging (default: WARNING)')
args = parser.parse_args()

#parse config
config = ConfigParser.SafeConfigParser()
config.read(['toodledo2growl.cnf'])

# config logging
numeric_level = getattr(logging, args.loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level)

# create Toodledo Client
app_id = config.get('credential', 'app_id')
app_token = config.get('credential', 'app_token')
logging.debug(': '.join(['Client app_id', app_id]))
logging.debug(': '.join(['Client app_token', app_token]))
api = ApiClient(app_id=app_id, app_token=app_token)
logging.info('created Toodledo Client')

# Toodledo Authentication
email = config.get('credential', 'email')
password = config.get('credential', 'password')
logging.debug(': '.join(['Auth email', email]))
logging.debug(': '.join(['Auth password', password]))
api.authenticate(email, password)
logging.info('Auth Toodledo')

# Get AccountInfo
account_info = api.getAccountInfo()
logging.debug(': '.join(['AccountInfo', str(account_info)]))

# Get Task list from Toodledo
task_list = api.getTasks(fields="duedate,star,priority")
logging.info(': '.join(['Got task list', str(len(task_list))]))

# Register to Growl
growl = gntp.notifier.GrowlNotifier(
    applicationName="toodledo2growl",
    notifications=["Task"],
    defaultNotifications=["Task"],
)
growl.register()
logging.info('Register growl')

# Send Notify to Growl
notify_icon = config.get('icon', 'notify')
for hot_task in _HotlistFilter(account_info, task_list):
    duedate = datetime.fromtimestamp(float(hot_task.duedate))
    growl.notify(
        noteType="Task",
        title=hot_task.title,
        description=duedate.strftime("DueDate: %Y/%m/%d"),
        icon=open(notify_icon, 'rb').read(),
        sticky=False,
        priority=1,
    )
    logging.info(': '.join(['notify sended', hot_task.title]))
# end
logging.info('end')
