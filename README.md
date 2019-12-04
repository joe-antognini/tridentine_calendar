# Tridentine liturgical calendar calculator

This code will calculate the feasts and ferias using the 1962 Roman Catholic
calendar rubrics.  The code can export the resulting calendar as an `.ics` file
which can then be imported by any calendar application, including Google
Calendar, iCalendar, and Yahoo Calendar.  Some events which are not part of the
1962 rubrics are included on the calendar as well.  These are traditionally
observed feasts and ferias or popular feasts on the modern calendar such as the
Feast of Our Lady of Guadalupe, Plough Monday, and the Feast of St. Brigid.  In
the case that two feasts or ferias coincide, the lower-ranking feast or feria is
prepended with '›'.  Non-liturgical events are preprended with '»'.

A preview of the calendar can be found here: https://joe-antognini.github.io/tridentine-calendar/

You can subscribe to the calendar using these links:

* This link for an HTTP friendly calendar: `webcal://joe-antognini.github.io/assets/ical/html_tridentine_calendar.ics`
* This link for a plaintext friendly calendar: `webcal://joe-antognini.github.io/assets/ical/tridentine_calendar.ics`

If you'd like to generate the calendar yourself, follow the instructions below:

## Requirements

* Python 3
* icalendar

## Installation

Clone the repository to a directory of your choice:

```
$ git clone git@github.com:joe-antognini/tridentine_calendar.git
```

Then install using pip

```
pip install -e tridentine_calendar/
```

## Usage

```
$ tridentine_calendar --output=my_calendar.ics 2019 2020
```

************

☩  Stat crux dum volvitur orbis. ☩  

☧ 
