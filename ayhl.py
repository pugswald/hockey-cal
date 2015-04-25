#!/usr/bin/python
from datetime import datetime, timedelta
from icalendar import Calendar, Event, Alarm
import xlrd
import sys

def process_xls(filename):
    wb = xlrd.open_workbook(filename)
    sheet = wb.sheet_by_index(0)
    calendar = Calendar()
    calendar.add('x-wr-calname','Schedule for U8 Summer Hockey 2015')
    for irow in range(sheet.nrows):
        row = sheet.row(irow)
        basedate = xlrd.xldate_as_tuple(row[1].value, wb.datemode)
        (hh, mmxx) = row[3].value.split(':')
        hh = int(hh)
        mm = int(mmxx[:2])
        xx = mmxx[2:]
        if xx == 'PM': 
            hh += 12
        basedt = list(basedate[:3]) + [hh, mm]
        tstamp = datetime(*basedt)
        uid = tstamp.strftime('%Y%m%d%H%M')+'@pugswald.com'
        event = Event()
        event.add('uid', uid)
        event.add('dtstart', tstamp)
        event.add('summary', 'AYHL U8 Hockey %s'%row[2].value)
        event.add('dtend', tstamp + timedelta(minutes=60))
        event.add('location', row[5].value)
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
