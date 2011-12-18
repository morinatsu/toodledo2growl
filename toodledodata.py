import time
from datetime import datetime, timedelta

def _local_date(string):
    dt = datetime.strptime(string[0:25], '%a, %d %b %Y %H:%M:%S')
    return dt + timedelta(hours=6) + timedelta(seconds=_local_time_offset())

def _local_time_offset():
    """Return offset of local zone from GMT"""
    if time.localtime().tm_isdst and time.daylight:
        return -time.altzone
    else:
        return -time.timezone

def _date(string):
    return datetime.st

def _boolstr(string):
    return bool(int(string))

def flatten(x):
    result = []
    if not hasattr(x, "__iter__"):
        result.append(x)
    else:
        for el in x:
            if hasattr(el, "__iter__") and not isinstance(el, basestring):
                result.extend(flatten(el))
            else:
                result.append(el)
    return result

class ToodledoData(object):
    _typemap = {
            'server': {
                'unixtime': int,
                'date': _local_date,
                'tokenexpires': float
                },
            'folder': {
                'id': int,
                'name': str,
                'archived': _boolstr,
                'private': _boolstr,
                'order': int
                },
            'context': {
                'id': int,
                'name': str,
                'def': _boolstr,
                },
            'goal': {
                'id': int,
                'name': str,
                'note': str,
                'level': int,
                'contributes': int,
                'archived': _boolstr
                },
            'location': {
                'id': int,
                'name': str,
                'description': str,
                'lat': float,
                'lon': float
                },
            'account': {
                'userid': str,
                'alias': str,
                'pro': _boolstr,
                'dateformat': int,
                'timezone': int,
                'hidemonths': int,
                'hotlistpriority': int,
                'hotlistduedate': int,
                'hotliststar': _boolstr,
                'hotliststatus': _boolstr,
                'showtabnums': _boolstr,
                'lastedit_folder': str,
                'lastedit_context': str,
                'lastedit_goal': str,
                'lastedit_location': str,
                'lastedit_task': str,
                'lastdelete_task': str,
                'lastedit_notebook': str,
                'lastdelete_notebook': str,
                'lastaddedit': str,
                'lastdelete': str,
                'lastfolderedit': str,
                'lastcontextedit': str,
                'lastgoaledit': str,
                'lastnotebookedit': str,
                },
            'task': {
                'id': int,
                'title': unicode,
                'modified': str,
                'completed': str,
                'folder': int,
                'context':  str,
                'goal': str,
                'location': int,
                'priority': int,
                'star': _boolstr,
                'tag': str,
                'remind': str,
                'repeat': str,
                'repeatfrom': int,
                'duedate': str,
                'duedatemod': str,
                'startdate': str,
                'duetime': str,
                'starttime': str,
                'length': int,
                'status': int,
                'timer': int,
                'timeron': str,
                'note': unicode,
                'meta': str,
                'added': str,
                'parent': int,
                'children': int,
                'title': unicode,
                'modified': str,
                'reminder': int,
                'rep_advanced': str,
                'stamp': str
                },
            'notebook': {
                'id': int,
                'folder': int,
                'added': str,
                'modified': str,
                'title': str,
                'text': str,
                'private': _boolstr,
                'stamp': str,
                },
            }

    def __init__(self, node=None):
        typemap = ToodledoData._typemap[node.tag]
        for elem in node.getchildren():
            self.__dict__[elem.tag] = typemap[elem.tag](elem.text)
        for a in node.attrib:
            self.__dict__[a] = typemap[a](node.attrib[a])
        if node.text and not node.text.isspace() :
            self.title = node.text

    def __str__(self):
        output = ["%s: %s" % (k, v) for (k, v) in self.__dict__.iteritems()]
        return '\n'.join(output)

    def __repr__(self):
        return str(self.__dict__)
