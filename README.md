# Tridentine liturgical calendar calculator

This code will calculate the feasts and ferias using the 1962 Roman Catholic calendar.  The code can
export the resulting calendar as an `.ics` file which can then be imported by any calendar
application, including Google Calendar, iCalendar, and Yahoo Calendar.  Some events
which are not part of the 1962 rubrics are included as well.  A few examples include the Feast of
Our Lady of Guadalupe, Plough Monday, and the Feast of St. Brigid.

To subscribe to this calendar, use this link:

[webcal://joe-antognini.github.io/assets/ics/liturgical_calendar.ics](webcal://joe-antognini.github.io/assets/ics/liturgical_calendar.ics)

Or, if you'd like to generate the calendar yourself, follow the instructions below:

## Requirements

* Python 3
* icspy

## Usage

```
$ python litcal.py --year=2019 --file=my_calendar.ics
```
