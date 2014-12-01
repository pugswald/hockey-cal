#!/usr/bin/env python
import cgi
from datetime import datetime, timedelta
from icalendar import Calendar, Event, Alarm
from lxml import html, etree
import requests
import sys

### TODO: Remove after debugging complete
import cgitb
cgitb.enable()
###



def html_to_ical(html_string):
    """Convert an html string from the pointstreak website to ical format
    
    Args: html_string - String representing the entire pointstreak schedule page
    
    Returns: Calendar object representing schedule
    """
    tree = html.fromstring(html_string)
    team = tree.xpath("//title")[0].text_content().split('-')[0].strip()
    schedule_tables = tree.xpath("//table/tr/td[contains(.,'Team Schedule')]")
    # First match is the table that contains all tables, second is the header in a td
    schedule_table = schedule_tables[1].getparent().getparent().getnext()
    # Get home v away, date, time, rink
    now = datetime.now()
    calendar = Calendar()
    calendar.add('x-wr-calname','Schedule for {}'.format(team))
    events = []
    for row in schedule_table.iter('tr'):
        try:
            #print etree.tostring(row)
            rink = row[4].text_content()
            if rink.startswith('final'):
                 # Game is already played
                continue
            rink = rink.strip()
            home = row[0].text_content()
            away = row[1].text_content()
            date_str = '{} {} {}'.format(row[2].text_content(), row[3].text_content(),
                                            now.year)
            tstamp = datetime.strptime(date_str, "%a, %b %d %I:%M %p %Y")
            # For whatever reason, the year is never printed
            if tstamp < now:
                tstamp.replace(year = tstamp.year + 1)
            uid = tstamp.strftime('%Y%m%d%H%M')+'@pugswald.com'
            event = Event()
            event.add('uid', uid)
            event.add('dtstart', tstamp)
            event.add('summary', 'Hockey game {} vs {}'.format(home,away))
            event.add('dtend', tstamp + timedelta(minutes=90))
            event.add('location', rink)
            alarm = Alarm()
            alarm.add('action', 'AUDIO')
            alarm.add('trigger', timedelta(minutes=-60))
            event.add_component(alarm)
            calendar.add_component(event)
            events.append('{} vs {} at {} {}'.format(home, away, tstamp.isoformat(), 
                                                     rink))
        except:
            #print sys.exc_info()
            pass # This block is not good data
            
    #print etree.tostring(schedule_table)
    #print schedule_table[1].text_content()
    #print events
    #print calendar.to_ical()
    return calendar
    
def get_html_schedule(url):
    """Read the schedule as an html page and return an html string
    """
    r = requests.get(url)
    return r.text

def main():
    print "Content-Type: text/calendar; charset=utf-8"
    print
    html_sched = get_html_schedule('http://www.pointstreak.com/players/players-team-schedule.html?teamid=525046&seasonid=13420')
    ical_sched = html_to_ical(html_sched)
    print ical_sched.to_ical()

if __name__ == "__main__":
    main()
