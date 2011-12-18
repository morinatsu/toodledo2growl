from plex import *
import parsedatetime.parsedatetime as pdt
from time import mktime
from StringIO import StringIO

p = pdt.Calendar()

letter = Range("AZaz")
digit = Range("09")
apos = Str("'")
dash = Str("-")
comma = Str(",")
period = Str(".")
slash = Str("/")
underscore = Str("_")
parens = Any("()")
formatting = Any("'-,./_():;?\\|!")
word = Rep1(letter | digit | parens | dash | slash) + Rep(letter | digit | apos | dash | comma | period | slash | underscore | formatting | parens)
number = Rep1(digit)
space = Any(" \t")
newline = Any("\n\r")
quote = Str("'")
doublequote= Str('"')
freetext = Alt( Rep1(word) + Rep(space + word),
 quote + Rep1(word) + Rep(space + word) + quote,
 doublequote + Rep1(word) + Rep(space + word) + doublequote)

folder = Alt(Bol, space) + Str("*") + Rep1(freetext)
context = Alt(Bol, space) + Str("@") + Rep1(freetext)
excl = Str("!")
priority = Alt(Bol, space) + Rep1(excl)
star = Alt(Bol, space) + Str("*")
#datefield = digit + digit + digit + digit + Str("/", "-") + digit + digit + Str("/", "-") + digit + digit
datefield = freetext
duedate = Alt(Bol, space) + Str("#") + datefield
startdate = Alt(Bol, space) + Str(">") + datefield
goal = Alt(Bol, space) + Str("+") + Rep1(freetext)
status = Alt(Bol, space) + Str("$") + Rep1(freetext)
#tagname = Rep1(word) + Opt(Str(",")) + Opt(space)
tag = Alt(Bol, space) + Str("%") + Rep1(word) + Rep(Str(",") + Opt(space) + word)
timefield = Rep1(number) + Opt(Str(":") + Rep1(number)) + Opt(space) + Str("AM", "PM", "am", "pm")
duetime = Alt(Bol, space) + Str("=") + Rep1(timefield)
starttime = Alt(Bol, space) + Str("^") + Rep1(timefield)
location = Alt(Bol, space) + Str("-") + Rep1(freetext)
durationfield = freetext
length = Alt(Bol, space) + Str("~") + Rep1(durationfield)
reminder = Alt(Bol, space) + Str(":") + Rep1(durationfield)
note = Alt(Bol, space) + Str("?") + Rep1(freetext)

lex = Lexicon([
    (space, IGNORE),
    (newline, 'newline'),
    (freetext, 'title'),
    (folder, 'folder'),
    (context, 'context'),
    (priority, 'priority'),
    (duedate, 'duedate'),
    (startdate, 'startdate'),
    (goal, 'goal'),
    (status, 'status'),
    (tag, 'tag'),
    (duetime, 'duetime'),
    (starttime, 'starttime'),
    (location, 'location'),
    (length, 'length'),
    (reminder, 'reminder'),
    (note, 'note'),
])

def rationalize(task):
    for k in task.keys():
        task[k] = task[k].strip()
        if k in ['folder', 'context', 'duedate', 'startdate', 'goal', 'location', 'status', 'tag', 'duetime', 'starttime', 'length', 'reminder', 'note']:
            task[k] = task[k][1:]
        if task[k][0] == '"' and task[k][-1] == '"':
            task[k] = task[k][1:-1]
        if k in ['duedate', 'startdate', 'duetime', 'starttime']:
            task[k] = mktime(p.parse(task[k])[0])
        if k == 'priority': task[k] = len(task[k])
        return task

def parse(task):
    r = StringIO(task)
    scanner = Scanner(lex, r, "raw task")
    parsedtask = {}
    while 1:
        token = scanner.read()
        if token[0] == 'newline' or token[0] is None:
            if len(parsedtask.keys()) > 0:
                return rationalize(parsedtask)
        else:
            parsedtask[token[0]] = token[1]
