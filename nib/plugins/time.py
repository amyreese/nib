import datetime
import time

from nib import jinja

@jinja('time')
def timeformat(t=None, f='%Y-%m-%d %I:%M %p'):
    if t is None:
        t = time.gmtime()
    elif isinstance(t, datetime.date) or isinstance(t, datetime.datetime):
        t = t.timetuple()
    elif isinstance(t, float):
        t = time.gmtime(t)

    s = time.strftime(f, t)
    return s

@jinja('atomtime')
def atomtimeformat(t=None, f='%Y-%m-%dT%I:%M:%SZ'):
    return timeformat(t,f)

@jinja('rsstime')
def rsstimeformat(t=None, f='%a, %d %b %Y %I:%M:%S GMT'):
    return timeformat(t,f)

@jinja('date')
def dateformat(t=None, f='%Y-%m-%d'):
    return timeformat(t,f)

@jinja('longdate')
def longdateformat(t=None, f='%B %d, %Y'):
    return timeformat(t, f)

