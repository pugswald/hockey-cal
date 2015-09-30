#!/usr/bin/python
from datetime import datetime, timedelta
from icalendar import Calendar, Event, Alarm
import xlrd
import sys

def get_hhmm(time_str):
    """Parse a time str and return a list [hh, mm]
    The time str is usually "2:15PM"
    """ 
    (hh, mmxx) = time_str.split(':')
    hh = int(hh)
    mm = int(mmxx[:2])
    xx = mmxx[2:]
    if xx == 'PM': 
        hh += 12
    return [hh, mm]


def process_xls(filename):
    wb = xlrd.open_workbook(filename)
    sheet = wb.sheet_by_index(0)
    calendar = Calendar()
    calendar.add('x-wr-calname','Schedule for U8 Adv Winter Hockey 2015')
    for irow in range(sheet.nrows):
        row = sheet.row(irow)
        evt_desc = None
        if row[0].value == "U8 Advanced":
            evt_desc = row[0].value
        if row[1].value == "Group 1":
            evt_desc = row[1].value
        if evt_desc is None:
            continue
        basedate = xlrd.xldate_as_tuple(row[3].value, wb.datemode)
        """
        (hh, mmxx) = row[4].value.split(':')
        hh = int(hh)
        mm = int(mmxx[:2])
        xx = mmxx[2:]
        if xx == 'PM': 
            hh += 12
        basedt = list(basedate[:3]) + [hh, mm]
        """
        basedt = list(basedate[:3]) + get_hhmm(row[4].value)
        tstamp = datetime(*basedt)
        basedt_end = list(basedate[:3]) + get_hhmm(row[5].value)
        tstamp_end = datetime(*basedt_end)
        uid = tstamp.strftime('%Y%m%d%H%M')+'@pugswald.com'
        event = Event()
        event.add('uid', uid)
        event.add('dtstart', tstamp)
        event.add('summary', 'AYHL Hockey - %s'%evt_desc)
        event.add('dtend', tstamp_end)
        event.add('location', row[6].value)
        alarm = Alarm()
        alarm.add('action', 'DISPLAY')
        alarm.add('description', 'Reminder')
        alarm.add('trigger', timedelta(minutes=-45))
        event.add_component(alarm)
        calendar.add_component(event)
    print calendar.to_ical()

def main():
    process_xls(sys.argv[1])

if __name__ == "__main__":
    main()
