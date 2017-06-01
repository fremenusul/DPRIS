import calendar
import datetime
import tz2ntz
import models
import snippets

def buildcalendar(platoon, soldier_data):

    cal = calendar.Calendar()
    # date object
    current_month = datetime.datetime.today()
    # get current month by name

    # build the number of days in a month
    today = tz2ntz.tz2ntz(current_month, 'UTC', 'US/Pacific')
    monthdates = [x for x in cal.itermonthdays(today.year, today.month) if x != 0]
    # get current day fixed

    # TODO(Shangpo) Add filter to grab this current month only. Investigate why filters don't work
    holder = []
    startdate = snippets.get_first_day(today)
    a_query = models.Attendance.query(models.Attendance.soldier_key == soldier_data.key.urlsafe())
    attendance_data = a_query.fetch()

    p = []
    a = []
    t = []
    dev = []
    datelist = []
    for y in attendance_data:
        if y.attendDate < startdate:
            continue
        day_num = int(datetime.datetime.strftime(y.attendDate, '%d'))
        value = y.attendValue
        if value == 'T':
            t.append(1)
        elif value == 'HP':
            t.append(0.5)
            p.append(1)
        elif value == 'H':
            t.append(0.5)
        elif value == '/':
            dev.append(1)
        elif value == 'A':
            a.append(1)
        elif value == 'P':
            p.append(1)
        datelist.append((day_num, value, y.key.urlsafe()))

    present = sum(p)
    absent = sum(a)
    training = sum(t)
    training_len = len(t)
    devday = sum(dev)
    totalattend = present + training
    # subtractdays = (present + absent + training_len) - devday
    subtractdays = len(monthdates) - devday
    actual_percent = '{0:.0f}%'.format(totalattend / subtractdays * 100)
    holder.append((soldier_data, datelist, present, absent, training, actual_percent))
    return holder, monthdates