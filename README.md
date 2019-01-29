# Tridentine liturgical calendar calculator

This code will calculate the feasts and ferias using the 1962 Roman Catholic calendar rubrics.  The
code can export the resulting calendar as an `.ics` file which can then be imported by any calendar
application, including Google Calendar, iCalendar, and Yahoo Calendar.  Some events which are not
part of the 1962 rubrics are included on the calendar as well.  These are traditionally observed
feasts and ferias or popular feasts on the modern calendar such as the Feast of Our Lady of
Guadalupe, Plough Monday, and the Feast of St. Brigid.  In the case that two feasts or ferias
coincide, the lower-ranking feast or feria is prepended with '›'.  Non-liturgical events are
preprended with '»'.

A preview of the calendar can be found here: https://joe-antognini.github.io/tridentine-calendar/

If you'd like to generate the calendar yourself, follow the instructions below:

## Requirements

* Python 3
* icalendar

## Usage

```
$ python tridentine_calendar.py --output=my_calendar.ics 2019
```
