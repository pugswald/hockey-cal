from datetime import datetime
from unittest import TestCase
from pointstreak import html_to_ical

class PointstreakTest(TestCase):
    def test_html(self):
        with open('test/sample.html') as sample:
            html_string = sample.read()
        c = html_to_ical(html_string)
        self.assertEqual(c['X-WR-CALNAME'], 'Schedule for Lodos')
        e = c.walk('vevent')[0]
        self.assertEqual(e['DTSTART'].dt, datetime(2014,12,06,21,50))